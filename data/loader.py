from importlib import resources
import csv
from typing import Any
from io import StringIO

from .types import ElementMapper, Table1Row, Table3Row


def transform_tsv_set_value(val: Any) -> frozenset|list[ElementMapper]:
    match val:
        case None|"":
            return frozenset()
        case str():
            eles = [list(x.strip()) for x in val.split(",")]
            transformed = []
            for ele in eles:
                match ele:
                    case [sub, idx] if sub.isalpha() and idx.isnumeric():
                        xformed = {"subscript": sub, "index": int(idx), "super": None}
                    case [dig1] if dig1.isnumeric():
                        xformed = {"subscript": None, "index": int(dig1), "super": None}
                    case [dig1, dig2] if dig1.isnumeric() and dig2.isnumeric():
                        xformed = {"subscript": None, "index": int("".join(ele)), "super": None}
                    case [sub, *idx, carrot, super] if sub.isalpha() and "".join(idx).isnumeric() and carrot == "^" and super.isnumeric():
                        xformed = {"subscript": sub, "index": int("".join(idx)), "super": int(super)}
                    case _:
                        raise ValueError(f"Unable to transform set value {ele}")
                transformed.append(xformed)
            return transformed
        case _:
            raise ValueError(f"Unable to transform set value {val}")

def load_tsv_to_buffer(name: str) -> StringIO:
    if not name.endswith(".tsv"):
        name = f"{name}.tsv"
    text = resources.read_text("data.tsvs", name)
    return StringIO(text)

def parse_tsv_to_records(name: str) -> list[dict[str, Any]]:
    buffer = load_tsv_to_buffer(name)
    parser = csv.reader(buffer, delimiter="\t")
    column_names = next(parser)
    loaded = []
    for row in parser:
        record = {k:v for k,v in zip(column_names, row)}
        loaded.append(record)
    return loaded

def records_elt(name: str) -> list[dict[str, Any]]:
    """Performs Extract load transform on records of tsv.
    
    Args:
        name: The name of the tsv in tsvs folder.

    Returns:
        List of dictionaries representing the rows.
    """
    loaded = parse_tsv_to_records(name)
    name = name.replace(".tsv","")
    match name:
        case "table1":
            ops = {
                "Organization": lambda x: x,
                "Activity ID": int,
                "Minimum Execution Time": int,
                "Maximum Execution Time": int,
                "Required Resource Set": transform_tsv_set_value,
                "Sent Resource Set": transform_tsv_set_value,
                "Pre-activities": transform_tsv_set_value,
            }
        case "table3":
            ops = {
                "Resource Type": lambda x: x,
                "Resource ID": transform_tsv_set_value,
                "Meaning": lambda x: x,
                "Property": lambda x: x,
                "Initial Number": lambda x: int(x) if x.isnumeric() else None,
            }
        case _:
            raise ValueError(f"No transformation for {name}")
    transformed = [
        {
                k: ops[k](v) for k,v in x.items()
        } for x in loaded
    ]
    return transformed

def load_table1() -> list[Table1Row]:
    return records_elt("table1")

def load_table3() -> list[Table3Row]:
    return records_elt("table3")