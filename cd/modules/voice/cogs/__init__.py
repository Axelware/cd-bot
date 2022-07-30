from __future__ import annotations

from typing import TYPE_CHECKING

from .effects import *
from .play import *
from .player import *
from .queue import *


if TYPE_CHECKING:
    from cd.bot import SkeletonClique


async def setup(bot: SkeletonClique) -> None:
    await bot.add_cog(Effects(bot))
    await bot.add_cog(Play(bot))
    await bot.add_cog(Player(bot))
    await bot.add_cog(Queue(bot))
