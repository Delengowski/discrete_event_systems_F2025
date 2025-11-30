"""My objects for verifying the algorithms."""

from dataclasses import dataclass
from typing import Literal


@dataclass(slot=True, frozen=True, repr=False)
class ResourcePlace:
    rtype: Literal["External", "Internal"]
    idx: int
    prop: Literal["Resuable", "Consumable"]
    initial_number: int | None
    super_idx: int | None

    def __repr__(self) -> str:
        if self.super_idx is not None:
            super_idx = f"^{self.super_idx}"
        else:
            super_idx = ""
        prefix = "p" if self.prop == "Consumable" else "P"
        return f"{type(self)}({prefix}_{self.idx}{super_idx})"


@dataclass(slot=True, frozen=True, repr=False)
class Activity:
    idx: int
    t_min: int
    t_max: int
    rss: set
    srs: set
    pa: set

    def __repr__(self) -> str:
        return f"{type(self)}(t_{t.idx})"
