from data import records_elt


def test_table1_elt():
    out = records_elt("table1")
    assert len(out) == 30

    # random assertions not evaluating the whole thing
    row = out[10]
    assert row["Organization"] == "Emergency Command Center"
    assert row["Activity ID"] == 11
    assert row["Minimum Execution Time"] == 5
    assert row["Maximum Execution Time"] == 8
    assert row["Required Resource Set"] == [
        {"subscript": "m", "index": 6, "super": None},
        {"subscript": "m", "index": 7, "super": None},
        {"subscript": "m", "index": 8, "super": None},
    ]
    assert row["Sent Resource Set"] == frozenset()
    assert row["Pre-activities"] == [{"subscript": None, "index": 10, "super": None}]

    row = out[3]
    assert row["Organization"] == "Police Station"
    assert row["Activity ID"] == 4
    assert row["Minimum Execution Time"] == 5
    assert row["Maximum Execution Time"] == 10
    assert row["Required Resource Set"] == [
        {"subscript": "r", "index": 3, "super": 2},
        {"subscript": "r", "index": 5, "super": 2},
    ]
    assert row["Sent Resource Set"] == [{"subscript": "r", "index": 3, "super": 2}]
    assert row["Pre-activities"] == [{"subscript": None, "index": 3, "super": None}]


def test_table3_elt():
    out = records_elt("table3")
    assert len(out) == 13

    # random assertions not evaluating the whole thing
    row = out[10]
    row["Resource Type"] == "External"
    row["Resource ID"] == [{"subscript": "r", "index": 1, "super": None}]
    row["Meaning"] == "ferry boat"
    row["Property"] == "Resuable"
    row["Initial Number"] == 1

    row = out[3]
    row["Resource Type"] == "Internal"
    row["Resource ID"] == [{"subscript": "m", "index": 1, "super": None}]
    row["Meaning"] == "emergency information"
    row["Property"] == "Consumable"
    row["Initial Number"] == None
