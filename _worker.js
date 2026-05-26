export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = decodeURIComponent(url.pathname);

    const commonHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": "no-store",
      "X-AliceTV-Source": "github-raw-proxy"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: commonHeaders
      });
    }

    if (path === "/" || path === "") {
      return new Response("AliceTV update source OK\n", {
        status: 200,
        headers: {
          ...commonHeaders,
          "Content-Type": "text/plain; charset=utf-8"
        }
      });
    }

    if (path.includes("..")) {
      return new Response("Bad request", {
        status: 400,
        headers: commonHeaders
      });
    }

    let upstream = "";

    if (
      path === "/version.json" ||
      path.startsWith("/templates/") ||
      path.startsWith("/m3u/") ||
      path.startsWith("/channels/")
    ) {
      upstream = "https://raw.githubusercontent.com/Jennie567/alicetv-update/main" + path;
    } else if (path.startsWith("/logos/")) {
      const name = path.replace("/logos/", "");
      upstream = "https://raw.githubusercontent.com/Jennie567/icon/main/TV/" + name;
    } else {
      return new Response("Not found", {
        status: 404,
        headers: commonHeaders
      });
    }

    try {
      const resp = await fetch(upstream, {
        headers: {
          "User-Agent": "AliceTV-Update-Proxy"
        }
      });

      if (!resp.ok) {
        return new Response("Upstream unavailable", {
          status: resp.status,
          headers: commonHeaders
        });
      }

      let contentType = "text/plain; charset=utf-8";

      if (path.endsWith(".json")) {
        contentType = "application/json; charset=utf-8";
      } else if (path.endsWith(".m3u")) {
        contentType = "audio/x-mpegurl; charset=utf-8";
      } else if (path.endsWith(".txt")) {
        contentType = "text/plain; charset=utf-8";
      } else if (path.endsWith(".png")) {
        contentType = "image/png";
      }

      return new Response(resp.body, {
        status: 200,
        headers: {
          ...commonHeaders,
          "Content-Type": contentType
        }
      });
    } catch (e) {
      return new Response("Proxy error", {
        status: 502,
        headers: commonHeaders
      });
    }
  }
};
