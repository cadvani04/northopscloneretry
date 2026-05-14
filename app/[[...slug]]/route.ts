import { readFile } from "fs/promises";
import path from "path";

const MIRROR_ROOT = path.join(process.cwd(), "mirror");

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
  const filePath = resolveMirrorHtml(slug);

  if (!filePath) {
    return new Response("Not Found", { status: 404 });
  }

  try {
    const raw = await readFile(filePath, "utf8");
    const html = patchWebflowHostHtml(raw);
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
