"""Pytests to assert we implement main paper algorithms correctly."""

from src.algorithms import dependency_set
from src.objects import load_activities, Activity
import pytest


@pytest.fixture(scope="module")
def T(request):
    return load_activities()


def test_dependency_set(T):
    ds = dependency_set(T)
    expected = {
        (Activity(2), Activity(10)),
        (Activity(4), Activity(5)),
        (Activity(4), Activity(6)),
        (Activity(5), Activity(6)),
        (Activity(18), Activity(23)),
        (Activity(17), Activity(22)),
    }
    assert ds == expected
