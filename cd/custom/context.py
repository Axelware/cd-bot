# Future
from __future__ import annotations

# Standard Library
from typing import TYPE_CHECKING, Any

# Packages
import discord
from discord.ext import commands

# My stuff
from cd import custom


if TYPE_CHECKING:
    # My stuff
    # noinspection PyUnresolvedReferences
    from cd.bot import CD


__all__ = (
    "Context",
)


class Context(commands.Context["CD"]):

    @property
    def voice_client(self) -> custom.Player | None:
        return getattr(self.guild, "voice_client", None)

    async def try_dm(self, *args: Any, **kwargs: Any) -> discord.Message | None:

        try:
            return await self.author.send(*args, **kwargs)
        except (discord.HTTPException, discord.Forbidden):
            try:
                return await self.reply(*args, **kwargs)
            except (discord.HTTPException, discord.Forbidden):
                return None