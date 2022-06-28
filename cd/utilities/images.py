# Future
from __future__ import annotations

# Standard Library
import asyncio
import pathlib
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from typing import TYPE_CHECKING, Literal, ParamSpec

# Packages
import filetype
import humanize
from jishaku.shell import SHELL, WINDOWS

# Local
from cd import exceptions


if TYPE_CHECKING:
    # Local
    from cd.bot import CD


__all__ = (
    "tshirt",
    "wiggle",
    "edit_image",
)


P = ParamSpec("P")
Method = Callable[[str], tuple[pathlib.Path, str]]


VALID_CONTENT_TYPES: list[str] = [
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
]
MAX_CONTENT_LENGTH: int = (2 ** 20) * 25
RESOURCES = pathlib.Path("cd/resources")

INPUT = "input"
OUTPUT = "output"


def tshirt(
    *,
    colour: Literal["gray", "wine"] = "gray",
) -> Method:
    return (
        lambda ext:
        (
            (RESOURCES / "tshirt"),
            f"./tshirt -r '130x130+275+175' {INPUT}.{ext} {colour}.png {OUTPUT}.{ext}"
        )
    )


def wiggle(
    *,
    frames: int = 25,
    delay: int = 5,
    direction: Literal["left", "right", "up", "down"] = "left",
    amount: int = 10
) -> Method:
    return (
        lambda ext:
        (
            (RESOURCES / "wiggle"),
            f"./wiggle -f {frames} -d {delay} -D {direction} -a {amount} {INPUT}.{ext} {OUTPUT}.gif"
        )
    )


async def edit_image(
    method: Method,
    /, *,
    image: str,
    bot: CD,
) -> None:

    with tempfile.TemporaryDirectory() as temp:
        temp = pathlib.Path(temp)

        async with bot.session.get(image) as response:
            if response.status != 200:
                raise exceptions.EmbedError(
                    description="Something went wrong while downloading your image. Try again later."
                )
            if int(response.headers.get("Content-Length") or "0") > MAX_CONTENT_LENGTH:
                raise exceptions.EmbedError(
                    description=f"Your image is too large to edit, it must be under "
                                f"**{humanize.naturalsize(MAX_CONTENT_LENGTH)}**."
                )
            if response.headers.get("Content-Type") not in VALID_CONTENT_TYPES:
                raise exceptions.EmbedError(
                    description="Your image does not have a valid file type."
                )

            image_bytes = await response.read()

        ext: str = filetype.guess_extension(image_bytes) or "png"
        (temp / f"{INPUT}.{ext}").write_bytes(image_bytes)

        resources, command = method(ext)

        for resource in resources.glob("**/*"):
            shutil.copy2(resource, temp)

        commands = [
            f"cd $(wslpath '{temp}'); " if WINDOWS else f"cd {temp}; "
        ]
        if ext == "gif":
            commands.append(
                f"mkdir frames; "
                f"convert -coalesce {INPUT}.gif frames/{INPUT}%04d.png; "
                f"find frames/ -maxdepth 1 -type f -exec {command.replace(f'{INPUT}.gif', '{}').replace(f'{OUTPUT}.gif', '{}')} \\;; "
                f"convert -delay 10 -loop 0 frames/{INPUT}*.png {OUTPUT}.gif; "
            )
        else:
            commands.append(command)

        p = subprocess.Popen(
            ["wsl", "bash.exe", "-c", "".join(commands)] if WINDOWS else [SHELL, "-c", "".join(commands)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = p.communicate()
        print(stdout)
        print(stderr)

        await asyncio.sleep(100)
