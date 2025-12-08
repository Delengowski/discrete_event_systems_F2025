import pytest
from src.objects import load_activities, Activity


@pytest.fixture(scope="module")
def T(request) -> list[Activity]:
    return load_activities()
