import numpy as np
import pytest
from sox.filter import CoulombCount
from sox.sensor import Sensor

dt = 1.0
capacity = 10  # Ah
initial_soc = 0.8


@pytest.fixture
def pulse_profile():
    time = np.arange(0, 100, dt)  # s
    current = np.where(time < max(time) / 2, 10, -10)  # A
    return time, current


@pytest.fixture
def expected_soc(pulse_profile):
    time, current = pulse_profile

    # coulomb count
    soc = np.zeros_like(time)
    soc[0] = initial_soc
    for i in range(len(time) - 1):
        soc[i + 1] = soc[i] - current[i] * dt / (capacity * 3600)
    return soc


def test_coulomb_count(pulse_profile, expected_soc):
    time, current = pulse_profile
    sensor = Sensor(name="current sensor", time=time, data=current)
    cc = CoulombCount(initial_soc, capacity, dt)

    estimated_soc = [initial_soc]
    for i in range(len(time) - 1):
        cc.predict(sensor.data[i])
        estimated_soc.append(cc.soc)

    assert np.allclose(expected_soc, estimated_soc, rtol=1e-3)
