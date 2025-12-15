"""Pytests to assert we implement main paper algorithms correctly."""

from src.algorithms import dependency_set
from src.objects import Activity
from src.invariant_reductions import apply_rules
import pytest

@pytest.fixture
def T_opt(T):
    return sorted(list(set(apply_rules(T))))

def test_dependency_set(T_opt):
    ds = dependency_set(T_opt)
    expected = [
        (Activity(2), Activity(10)),
        (Activity(4), Activity(5)),
        (Activity(4), Activity(6)),
        (Activity(5), Activity(6)),
        (Activity(17), Activity(22)),
        (Activity(18), Activity(23)),
    ]
    assert ds == expected
