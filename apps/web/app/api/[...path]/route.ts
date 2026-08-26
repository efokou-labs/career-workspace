const API_URL = process.env.API_URL || "http://localhost:8080";

type RouteContext = { params: Promise<{ path: string[] }> };

async function proxy(req: Request, context: RouteContext): Promise<Response> {
  const { path } = await context.params;
  const incoming = new URL(req.url);
  const target = `${API_URL}/${path.join("/")}${incoming.search}`;
  const headers = new Headers(req.headers);
  headers.delete("host");
  const body =
    req.method === "GET" || req.method === "HEAD" ? undefined : await req.arrayBuffer();
  const res = await fetch(target, { method: req.method, headers, body });
  const out = new Headers(res.headers);
  out.delete("content-encoding");
  out.delete("transfer-encoding");
  return new Response(res.body, { status: res.status, headers: out });
}

export async function GET(req: Request, context: RouteContext) {
  return proxy(req, context);
}

export async function POST(req: Request, context: RouteContext) {
  return proxy(req, context);
}
