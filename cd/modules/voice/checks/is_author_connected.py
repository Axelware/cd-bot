# Future
from __future__ import annotations

# Standard Library
from typing import Literal

# Packages
import discord
from discord.ext import commands
from discord.ext.commands._types import Check

# Local
from cd import custom, exceptions


__all__ = (
    "is_author_connected",
)


def is_author_connected() -> Check[custom.Context]:

    async def predicate(ctx: custom.Context) -> Literal[True]:

        assert isinstance(ctx.author, discord.Member)

        author_channel = ctx.author.voice and ctx.author.voice.channel
        player_channel = ctx.player and ctx.player.voice_channel

        if player_channel != author_channel:
            raise exceptions.EmbedError(
                description=f"You must be connected to {getattr(player_channel, 'mention', None)} to use this "
                            f"command."
            )

        return True

    return commands.check(predicate)
