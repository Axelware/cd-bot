# Future
from __future__ import annotations

# Packages
import discord

# My stuff
from core import values


__all__ = (
    "embed",
)


def embed(
    footer: str | None = None,
    footer_url: str | None = None,
    image: str | None = None,
    thumbnail: str | None = None,
    author: str | None = None,
    author_url: str | None = None,
    author_icon_url: str | None = None,
    title: str | None = None,
    description: str | None = None,
    url: str | None = None,
    colour: discord.Colour = values.ORANGE,
    emoji: str | None = None,
) -> discord.Embed:

    e = discord.Embed(colour=colour)

    if footer:
        e.set_footer(
            text=footer,
            icon_url=footer_url or discord.embeds.EmptyEmbed
        )

    if image:
        e.set_image(url=image)
    if thumbnail:
        e.set_thumbnail(url=thumbnail)

    if author:
        e.set_author(
            name=author,
            url=author_url or discord.embeds.EmptyEmbed,
            icon_url=author_icon_url or discord.embeds.EmptyEmbed
        )

    if title:
        e.title = title
    if description:
        e.description = f"{emoji} {values.ZWSP} {description}" if emoji else description
    if url:
        e.url = url

    return e
