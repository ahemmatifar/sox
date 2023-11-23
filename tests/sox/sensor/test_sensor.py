import copy

import numpy as np
import pytest
from sox.sensor import Drift, Normal, Offset, Scaling, Sensor, StuckAt

SEED = 123


@pytest.fixture
def time():
    return np.linspace(0, 10, 100).tolist()


@pytest.fixture
def data(time):
    return np.ones_like(time).tolist()


@pytest.fixture
def faults():
    return [
        Offset(offset=0.1, start_time=1, stop_time=2),
        Scaling(scale=2, start_time=3, stop_time=4),
        Drift(rate=0.1, start_time=5, stop_time=6),
        StuckAt(value=0, start_time=7, stop_time=8),
    ]


@pytest.fixture
def data_with_faults(time, data, faults):
    data_with_faults = []
    for t, d in zip(time, data):
        for fault in faults:
            d = fault.apply(t, d)
        data_with_faults.append(d)
    return data_with_faults


def test_default_sensor(time, data):
    sensor = Sensor(name="default", time=time, data=data)

    sensor_data = []
    try:
        while True:
            sensor_data.append(sensor.read())
    except IndexError as e:
        print(e)
    assert sensor_data == data


def test_sensor_with_faults(time, data, faults, data_with_faults):
    sensor = Sensor(name="faulty", time=time, data=data, faults=faults)

    sensor_data = []
    try:
        while True:
            sensor_data.append(sensor.read())
    except IndexError as e:
        print(e)
    assert sensor_data == data_with_faults
