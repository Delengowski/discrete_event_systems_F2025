from src.objects import ResourcePlace, load_activities, Activity


def test_load_activities():
    activities = load_activities()
    assert len(activities) == 30

    activity = activities[0]
    expected = Activity(
        1, "Police Station", 2, 4, frozenset(), frozenset(), frozenset()
    )
    assert activity.idx == expected.idx
    assert activity.org == expected.org
    assert activity.t_min == expected.t_min
    assert activity.t_max == expected.t_max
    assert activity.rss == expected.rss
    assert activity.srs == expected.srs
    assert activity.pa == expected.pa

    activity = activities[9]
    expected = Activity(
        10,
        "Emergency Command Center",
        3,
        5,
        frozenset(
            [
                ResourcePlace(
                    "r",
                    2,
                    "External",
                    "public communication device",
                    "Reusable",
                    1,
                ),
                ResourcePlace(
                    "m",
                    2,
                    "Internal",
                    "site conditions",
                    "Consumable",
                    None,
                ),
            ]
        ),
        frozenset(
            [
                ResourcePlace(
                    "r",
                    2,
                    "External",
                    "public communication device",
                    "Reusable",
                    1,
                ),
                ResourcePlace(
                    "m",
                    3,
                    "Internal",
                    "medical rescue instruction",
                    "Consumable",
                    None,
                ),
                ResourcePlace(
                    "m",
                    4,
                    "Internal",
                    "fire rescue instruction",
                    "Consumable",
                    None,
                ),
                ResourcePlace(
                    "m",
                    5,
                    "Internal",
                    "search EOD instruction",
                    "Consumable",
                    None,
                ),
            ]
        ),
        frozenset([9]),
    )
    assert activity.idx == expected.idx
    assert activity.org == expected.org
    assert activity.t_min == expected.t_min
    assert activity.t_max == expected.t_max
    assert activity.rss == expected.rss
    assert activity.srs == expected.srs
    assert activity.pa == expected.pa
