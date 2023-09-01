import pytest



@pytest.fixture
def example_fixture():
    return 1

def test_core_always_passes(example_fixture):
    assert example_fixture == 1

def test_core_always_fails(example_fixture):
    assert example_fixture == 2