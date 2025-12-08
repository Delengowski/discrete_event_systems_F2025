# from src.invariant_reductions import rule1, rule1_1, rule1_2, rule2
from src.invariant_reductions import rule1_1, rule1, rule1_2
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
    assert out == [(Activity(x) for x in (24, 25, 26, 27, 28))]
