import { readFile } from "fs/promises";
import path from "path";

const MIRROR_ROOT = path.join(process.cwd(), "mirror");

/** Shared Google Drive file (must be "Anyone with the link" can view). Used on Vercel when no CDN URL. */
const GOOGLE_DRIVE_HERO_FILE_ID = "17Skp3l5DgmFyd_rx-9mnYjI5kKpIOB77";
const GOOGLE_DRIVE_HERO_SRC = `https://drive.google.com/uc?export=download&id=${GOOGLE_DRIVE_HERO_FILE_ID}`;

/**
 * Hero video: local public/videos/0515.mov is too large for Vercel Hobby static limits.
 * - Local dev: unchanged mirror path /videos/0515.mov
 * - Vercel (VERCEL=1): replace with Google Drive direct link unless NORTHOPS_HERO_VIDEO_URL is set (CDN wins)
 */
function escapeHtmlAttrValue(value: string): string {
  return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;");
}

function injectHomeHeroVideoSrc(html: string, isHome: boolean): string {
  if (!isHome) return html;

  const cdnUrl = process.env.NORTHOPS_HERO_VIDEO_URL?.trim();
  const onVercel = Boolean(process.env.VERCEL);
  const url = cdnUrl || (onVercel ? GOOGLE_DRIVE_HERO_SRC : "");

  if (!url) return html;
  return html.replace(
    /src="\/videos\/0515\.mov"/,
    `src="${escapeHtmlAttrValue(url)}"`,
  );
}

/** Rewritten mirrored CSS no longer matches Webflow's SRI hash; browsers block the whole sheet. */
function stripSubresourceIntegrity(html: string): string {
  return html.replace(/\s+integrity=["'][^"']+["']/gi, "");
}

/**
 * Webflow hides nav/footer/CTA until IX adds `w-mod-ix3`; that often never fires off-domain
 * (localhost). Mark IX ready so layout matches production.
 */
function patchWebflowHostHtml(html: string): string {
  let out = stripSubresourceIntegrity(html);
  const ix = `<script>document.documentElement.classList.add("w-mod-ix3")</script>`;
  out = out.replace(/<body([^>]*)>/i, `<body$1>${ix}`);
  return out;
}

function resolveMirrorHtml(slug: string[] | undefined): string | null {
  const segments = slug?.filter(Boolean) ?? [];
  const relative =
    segments.length === 0
      ? "index.html"
      : path.join(...segments, "index.html");

  const absolute = path.join(MIRROR_ROOT, relative);
  const normalized = path.normalize(absolute);

  if (!normalized.startsWith(path.resolve(MIRROR_ROOT))) {
    return null;
  }

  return normalized;
}

export async function GET(
  _request: Request,
  context: { params: Promise<{ slug?: string[] }> },
) {
  const { slug } = await context.params;
  const segments = slug?.filter(Boolean) ?? [];
  const isHome = segments.length === 0;
  const filePath = resolveMirrorHtml(slug);

  if (!filePath) {
    return new Response("Not Found", { status: 404 });
  }

  try {
    const raw = await readFile(filePath, "utf8");
    let html = patchWebflowHostHtml(raw);
    html = injectHomeHeroVideoSrc(html, isHome);
    return new Response(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=0, must-revalidate",
      },
    });
  } catch {
    return new Response("Not Found", { status: 404 });
  }
}
