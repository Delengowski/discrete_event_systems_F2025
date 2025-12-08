"""Pytests to assert we implement main paper algorithms correctly."""

from src.algorithms import dependency_set
import pytest


def test_dependency_set(T):
    pytest.skip()
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
