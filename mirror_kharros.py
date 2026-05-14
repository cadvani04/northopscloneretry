#!/usr/bin/env python3
"""Mirror www.kharros.com (sitemap pages + static assets) for local viewing."""
from __future__ import annotations

import re
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
MIRROR_HTML = BASE / "mirror"
PUBLIC_ASSETS = BASE / "public" / "_assets"
SITEMAP = "https://www.kharros.com/sitemap.xml"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

ASSET_HOSTS = frozenset(
    {
        "cdn.prod.website-files.com",
        "d3e54v103j8qbb.cloudfront.net",
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "ajax.googleapis.com",
        "player.vimeo.com",
    }
)

ctx = ssl.create_default_context()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
        return r.read()


def asset_host(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower()


def should_mirror_asset(url: str) -> bool:
    try:
        h = asset_host(url)
        if h not in ASSET_HOSTS:
            return False
        if h == "player.vimeo.com" and "/video/" in urllib.parse.urlparse(url).path:
            return False
        p = urllib.parse.urlparse(url)
        path = p.path or ""
        if path in ("", "/"):
            return False
        return True
    except Exception:
        return False


def local_asset_path(url: str) -> Path:
    """Filesystem path for a mirrored absolute asset URL (query folded into filename)."""
    p = urllib.parse.urlparse(url)
    parts = [x for x in p.path.split("/") if x]
    if p.query and parts:
        last = parts[-1]
        if "." in last:
            base, ext_no_dot = last.rsplit(".", 1)
            ext = "." + ext_no_dot
        else:
            base, ext = last, ""
        qslug = re.sub(r"[^\w.-]+", "_", p.query).strip("_")[:80]
        parts[-1] = f"{base}__q_{qslug}{ext}"
    elif p.query:
        parts.append("root__q_" + re.sub(r"[^\w.-]+", "_", p.query).strip("_")[:80])
    rel = "/".join(parts)
    return PUBLIC_ASSETS / p.netloc / rel


def webpath_for(url: str) -> str:
    rel = local_asset_path(url).relative_to(BASE / "public").as_posix()
    return "/" + rel


def page_disk_path(page_url: str) -> Path:
    p = urllib.parse.urlparse(page_url)
    slug = (p.path or "/").rstrip("/") or ""
    if not slug or slug == "/":
        return MIRROR_HTML / "index.html"
    return MIRROR_HTML / slug.strip("/") / "index.html"


def sitemap_urls() -> list[str]:
    raw = fetch(SITEMAP).decode("utf-8", errors="replace")
    urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", raw, flags=re.I)
    out: list[str] = []
    for u in urls:
        u = u.strip()
        if not u.startswith("http"):
            u = "https://" + u.lstrip("/")
        out.append(u)
    return sorted(set(out))


def extract_html_asset_urls(html: str) -> set[str]:
    found: set[str] = set()
    for pat in (
        r'src\s*=\s*["\']([^"\']+)["\']',
        r'href\s*=\s*["\']([^"\']+)["\']',
        r'content\s*=\s*["\'](https?://[^"\']+)["\']',
    ):
        for m in re.finditer(pat, html, flags=re.I):
            u = m.group(1).strip()
            if u.startswith("//"):
                u = "https:" + u
            if not u.startswith("http"):
                continue
            u = u.split("#")[0]
            if should_mirror_asset(u):
                found.add(u)
    return found


def extract_css_urls(css: str, base_url: str) -> set[str]:
    found: set[str] = set()
    for m in re.finditer(r"url\(\s*['\"]?([^'\")\s]+)['\"]?\s*\)", css, flags=re.I):
        u = m.group(1).strip()
        if u.startswith(("data:", "#", "mailto:")):
            continue
        full = urllib.parse.urljoin(base_url, u).split("#")[0]
        if should_mirror_asset(full):
            found.add(full)
    return found


def strip_subresource_integrity(html: str) -> str:
    """Mirrored CSS is URL-rewritten so Webflow's integrity= no longer matches; strip it."""
    return re.sub(r'\s+integrity=["\'][^"\']+["\']', "", html, flags=re.I)


def rewrite_assets(body: str) -> str:
    """Replace mirrored absolute URLs with local /_assets/... paths."""

    def repl(m: re.Match[str]) -> str:
        u = m.group(0).split("#")[0]
        if not should_mirror_asset(u):
            return m.group(0)
        return webpath_for(u)

    pat = re.compile(
        r"https?://(?:"
        r"cdn\.prod\.website-files\.com/[^\s\"\'\)\>]*|"
        r"d3e54v103j8qbb\.cloudfront\.net/[^\s\"\'\)\>]*|"
        r"fonts\.googleapis\.com/[^\s\"\'\)\>]*|"
        r"fonts\.gstatic\.com/[^\s\"\'\)\>]*|"
        r"ajax\.googleapis\.com/[^\s\"\'\)\>]*|"
        r"player\.vimeo\.com/api/[^\s\"\'\)\>]*"
        r")",
        flags=re.I,
    )
    body = pat.sub(repl, body)
    for prefix in (
        "https://www.kharros.com",
        "http://www.kharros.com",
        "https://kharros.com",
        "http://kharros.com",
    ):
        body = body.replace(prefix, "")
    return body


def download_asset(url: str, log: bool = True) -> None:
    dest = local_asset_path(url)
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = fetch(url)
    if url.lower().rstrip("/").endswith(".css") or "/css/" in urllib.parse.urlparse(url).path:
        dest.write_text(data.decode("utf-8", errors="replace"), encoding="utf-8")
    else:
        dest.write_bytes(data)
    if log:
        print("  asset", url)


def main() -> None:
    MIRROR_HTML.mkdir(parents=True, exist_ok=True)
    PUBLIC_ASSETS.mkdir(parents=True, exist_ok=True)
    pages = sitemap_urls()
    print("Pages:", len(pages))

    page_html: dict[str, str] = {}
    for url in pages:
        page_html[url] = fetch(url).decode("utf-8", errors="replace")
        print("  page", url)

    assets: set[str] = set()
    for html in page_html.values():
        assets |= extract_html_asset_urls(html)

    css_todo = sorted(u for u in assets if ".css" in urllib.parse.urlparse(u).path.lower())
    seen_css: set[str] = set()

    while css_todo:
        u = css_todo.pop()
        if u in seen_css:
            continue
        seen_css.add(u)
        try:
            download_asset(u, log=True)
        except Exception as e:
            print("  !css", u, e)
            continue
        css_text = local_asset_path(u).read_text(encoding="utf-8", errors="replace")
        for nested in extract_css_urls(css_text, u):
            assets.add(nested)
            if ".css" in urllib.parse.urlparse(nested).path.lower() and nested not in seen_css:
                css_todo.append(nested)

    for u in sorted(assets):
        if u in seen_css:
            continue
        try:
            download_asset(u, log=True)
        except Exception as e:
            print("  !asset", u, e)

    for css_path in PUBLIC_ASSETS.rglob("*.css"):
        txt = css_path.read_text(encoding="utf-8", errors="replace")
        css_path.write_text(rewrite_assets(txt), encoding="utf-8")

    for url, html in page_html.items():
        path = page_disk_path(url)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            strip_subresource_integrity(rewrite_assets(html)),
            encoding="utf-8",
        )
        print("wrote", path.relative_to(BASE))

    print("Done. HTML in mirror/, assets in public/_assets/. Run: npm run dev")


if __name__ == "__main__":
    main()
