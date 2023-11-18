import numpy as np
import pytest
from sox.sensor import Drift, Fault, Offset, Scaling, StuckAt

SEED = 123
np.random.seed(SEED)

time = np.linspace(0, 10, 100)
random_values = np.random.random(100)


@pytest.fixture
def faults():
    return {
        "random": Fault(fault_probability=0.5, random_seed=SEED),
        "time_based": Fault(start_time=1, stop_time=2),
    }


@pytest.fixture
def offset():
    return Offset(offset=1, start_time=1, stop_time=2)


@pytest.fixture
def scaling():
    return Scaling(scale=2, start_time=1, stop_time=2)


@pytest.fixture
def drift():
    return Drift(rate=0.1, start_time=1, stop_time=2)


@pytest.fixture
def stuck_at():
    return StuckAt(value=0, start_time=1, stop_time=2)


def test_faults(faults):
    # random is active according to fault_probability, regardless of time
    is_active = [rand < faults["random"].fault_probability for rand in random_values]
    assert np.all([faults["random"].is_active(t) == a for (t, a) in zip(time, is_active)])

    # time_based is active between start_time and stop_time
    is_active = [faults["time_based"].start_time <= t <= faults["time_based"].stop_time for t in time]
    assert np.all([faults["time_based"].is_active(t) == a for (t, a) in zip(time, is_active)])

    # probability-based and time-based faults are mutually exclusive
    with pytest.raises(ValueError):
        Fault(fault_probability=0.5, start_time=1, stop_time=2)


def test_offset(offset):
    true_value = 1.0
    times = [0, 1, 3]
    expected_values = [true_value, true_value + offset.offset, true_value]

    for t, v in zip(times, expected_values):
        assert offset.apply(time=t, value=true_value) == v


def test_scaling(scaling):
    true_value = 1.0
    times = [0, 1, 3]
    expected_values = [true_value, true_value * scaling.scale, true_value]

    for t, v in zip(times, expected_values):
        assert scaling.apply(time=t, value=true_value) == v


def test_drift(drift):
    true_value = 1.0
    times = [0, 1, 2, 3]
    expected_values = [
        true_value,
        true_value,
        true_value + drift.rate * (2 - 1),
        true_value,  # back to true value at time=3
    ]

    for t, v in zip(times, expected_values):
        print(t, v)
        assert drift.apply(time=t, value=true_value) == v


def test_stuck_at(stuck_at):
    true_value = 1.0
    times = [0, 1, 2, 3]
    expected_values = [true_value, stuck_at.value, stuck_at.value, true_value]

    for t, v in zip(times, expected_values):
        assert stuck_at.apply(time=t, value=true_value) == v
