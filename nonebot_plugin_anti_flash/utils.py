import io
import mimetypes

import httpx
import magic
from nonebot import logger
from pydantic import FilePath, HttpUrl


async def save_image_from_url(
    url: HttpUrl, path: FilePath, filename: str, client: httpx.AsyncClient
):
    r = await client.get(url)
    img = io.BytesIO()
    async for b in r.aiter_bytes():
        img.write(b)
    img.seek(0)

    mime = magic.from_buffer(img.read(2048), mime=True)
    if mime.startswith("image/"):
        ext = mimetypes.guess_extension(mime)
    else:
        logger.warning(f"Unknown file type {mime}, skip saving for {url}.")
        return

    img.seek(0)
    with open(path / f"{filename}{ext}", mode="wb") as f:
        f.write(img.read())
