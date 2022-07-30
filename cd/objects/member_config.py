from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from cd import enums, utilities


if TYPE_CHECKING:
    from cd.bot import SkeletonClique


__all__ = (
    "MemberConfig",
    "MemberConfigData",
)


class MemberConfigData(TypedDict):
    user_id: int
    guild_id: int
    xp: int
    money: float


class MemberConfig:

    def __init__(self, bot: SkeletonClique, data: MemberConfigData) -> None:
        self.bot: SkeletonClique = bot

        self.user_id: int = data["user_id"]
        self.guild_id: int = data["guild_id"]
        self.xp: int = data["xp"]
        self.money: float = data["money"]

    def __repr__(self) -> str:
        return f"<Member user_id={self.user_id}, guild_id={self.guild_id}>"

    # Properties

    @property
    def level(self) -> int:
        return utilities.level(self.xp)

    @property
    def needed_xp(self) -> int:
        return utilities.needed_xp(self.level, self.xp)

    # Methods

    async def change_xp(self, operation: enums.Operation, /, amount: int) -> None:

        operations = [enums.Operation.Set, enums.Operation.Add, enums.Operation.Minus]
        if operation not in operations:
            raise ValueError(f"'change_xp' expects one of {operations}, got '{operation!r}'.")

        if operation == enums.Operation.Set:
            self.xp = amount
        elif operation == enums.Operation.Add:
            self.xp += amount
        elif operation == enums.Operation.Minus:
            self.xp -= amount

        await self.bot.db.execute(
            "UPDATE members SET xp = $1 WHERE user_id = $2 AND guild_id = $3",
            self.xp, self.user_id, self.guild_id
        )