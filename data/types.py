from typing import TypedDict, Literal

class ElementMapper(TypedDict):
    subscript: Literal["m", "r"]
    index: int
    super: int|None

Table1Row = TypedDict("Table1Row", {
    "Organization": Literal["Police Station", "Emergency Command Center", "EOD Team", "Fire Brigade", "Hospital"],
    "Activity ID": ElementMapper,
    "Minimum Execution Time": int,
    "Maximum Execution Time": int,
    "Required Resource Set": frozenset[ElementMapper],
    "Sent Resouce Set": frozenset[ElementMapper],
    "Pre-Activities": frozenset[ElementMapper],
})

Table3Row = TypedDict("Table3Row", {
    "Resource Type": Literal["External", "Internal"],
    "Resource ID": ElementMapper,
    "Meaining": str,
    "Property": Literal["Reusable", "Consumable"],
})