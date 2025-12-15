from src.invariant_reductions import rule1_1, rule1, rule1_2, rule2, apply_rules
from src.objects import Activity


def test_rule1(T):
    """This test is on the bare set of Activities from table 1, there may be
    situations where multiple rules apply and further tie breaker logic is applied."""
    out = rule1(T)
    assert out == [(Activity(12), Activity(13))]


def test_rule1_1(T):
    out = rule1_1(T)
    assert out == [(Activity(11), Activity(12), Activity(13))]


def test_rule1_2(T):
    out = rule1_2(T)
    assert out == []


def test_rule2(T):
    out = rule2(T)
    assert out == [(Activity(20), Activity(21)), (Activity(25), Activity(26))]


def test_overall_rule_application(T):
    out = sorted(list(set(apply_rules(T))))
    assert out == [
        Activity(1),
        Activity(2),
        Activity(3),
        Activity(4),
        Activity(5),
        Activity(6),
        Activity(7),
        Activity(8),
        Activity(9),
        Activity(10),
        Activity(frozenset([11,12,13])),
        Activity(14),
        Activity(15),
        Activity(16),
        Activity(17),
        Activity(18),
        Activity(frozenset([19,20,21])),
        Activity(22),
        Activity(23),
        Activity(frozenset([24,25,26,27,28])),
    ]
