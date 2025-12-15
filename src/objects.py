"""My objects for verifying the algorithms."""

from dataclasses import dataclass, field
from functools import total_ordering
from typing import Literal, Self
from data import load_table1, load_table3, ElementMapper


@dataclass(slots=True, frozen=True, repr=False)
class ResourcePlace:
    subscript: Literal["m", "r"]
    idx: int
    rtype: Literal["External", "Internal"] = field(compare=False, hash=False)
    meaning: str = field(compare=False, hash=False)
    prop: Literal["Resuable", "Consumable"] = field(compare=False, hash=False)
    initial_number: int | None = field(compare=False, hash=False)
    super_idx: int | None = field(default=None, compare=False, hash=False)

    def __repr__(self) -> str:
        if self.super_idx is not None:
            super_idx = f"^{self.super_idx}"
        else:
            super_idx = ""
        prefix = "p" if self.rtype == "internal" else "P"
        return f"{type(self).__name__}({prefix}_{self.idx}{super_idx})"


@total_ordering
@dataclass(slots=True, frozen=True, repr=False, order=False)
class Activity:
    idx: int | frozenset[Self]
    org: str | None = field(default=None, compare=False, hash=False)
    t_min: int | None = field(default=None, compare=False, hash=False)
    t_max: int | None = field(default=None, compare=False, hash=False)
    rss: frozenset[ResourcePlace] = field(
        default_factory=frozenset, compare=False, hash=False
    )
    srs: frozenset[ResourcePlace] = field(
        default_factory=frozenset, compare=False, hash=False
    )
    pa: frozenset[int] = field(default_factory=frozenset, compare=False, hash=False)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(t_{self.idx})"

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        match (self.idx, other.idx):
            case [int(), int()]:
                return self.idx < other.idx
            case [int(), frozenset()]:
                return self.idx < min(other.idx)
            case [frozenset(), int()]:
                return min(self.idx) < other.idx
            case [frozenset(), frozenset()]:
                return min(self.idx) < min(other.idx)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        match (self.idx, other.idx):
            case [int(), int()] | [frozenset(), frozenset()]:
                return self.idx == other.idx
            case [int(), frozenset()]:
                return frozenset([self.idx]) == other.idx
            case [frozenset(), int()]:
                return self.idx == frozenset([other.idx])


table1 = load_table1()
table3 = load_table3()

table3_mapper_to_resource = {
    (row["Resource ID"][0]["subscript"], row["Resource ID"][0]["index"]): row
    for row in table3
}


def process_resource_set_items(eles: list[ElementMapper]) -> frozenset[ResourcePlace]:
    resources = []
    for ele in eles:
        subscript = ele["subscript"]
        index = ele["index"]
        table3_info = table3_mapper_to_resource[(subscript, index)]
        resources.append(
            ResourcePlace(
                subscript=subscript,
                idx=index,
                rtype=table3_info["Resource Type"],
                meaning=table3_info["Meaning"],
                prop=table3_info["Property"],
                initial_number=table3_info["Initial Number"],
                super_idx=ele["super"],
            )
        )
    return frozenset(resources)


def load_activities() -> list[Activity]:
    activity_table = []
    for row in table1:
        org = row["Organization"]
        idx = row["Activity ID"]
        t_min = row["Minimum Execution Time"]
        t_max = row["Maximum Execution Time"]

        required_resource_set = row["Required Resource Set"]
        if required_resource_set:
            rss = process_resource_set_items(required_resource_set)
        else:
            rss = required_resource_set

        sent_resource_set = row["Sent Resource Set"]
        if sent_resource_set:
            srs = process_resource_set_items(sent_resource_set)
        else:
            srs = sent_resource_set

        pre_activities = row["Pre-activities"]
        if pre_activities:
            pa = frozenset(x["index"] for x in pre_activities)
        else:
            pa = pre_activities

        activity_table.append(Activity(idx, org, t_min, t_max, rss, srs, pa))
    return activity_table
