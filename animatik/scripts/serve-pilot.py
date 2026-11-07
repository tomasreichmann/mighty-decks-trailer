"""Serve the local A/B pilot, including byte-range requests for accurate seeking."""
from pathlib import Path

from aiohttp import web


PILOT = Path(__file__).resolve().parents[1] / "pilot"


async def index(request):
    return web.FileResponse(PILOT / "index.html", headers={"Cache-Control": "no-cache"})


async def variants(request):
    return web.FileResponse(PILOT / "variants.json", headers={"Cache-Control": "no-store"})


if __name__ == "__main__":
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/variants.json", variants)
    app.router.add_static("/files", PILOT / "files")
    web.run_app(app, host="127.0.0.1", port=3118)
