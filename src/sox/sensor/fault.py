import numpy as np


class Fault:
    """Base class for sensor faults

    Args:
        fault_probability (float): Probability of fault occurring.
        random_seed (int): Random seed for reproducibility.
        start_time (float): Start time of fault.
        stop_time (float): Stop time of fault.
    """

    def __init__(self, fault_probability=None, random_seed=None, start_time=None, stop_time=None):
        self.validate_inputs(fault_probability, start_time, stop_time)

        self.fault_probability = fault_probability
        self.start_time = start_time
        self.stop_time = stop_time

        if random_seed is not None:
            np.random.seed(random_seed)

    def is_active(self, time):
        """Returns True if fault is active at given time, False otherwise

        Args:
            time (float): Time in seconds.
        Returns:
            bool: True if fault is active at given time, False otherwise.
        """
        if self.fault_probability is not None:
            return np.random.random() < self.fault_probability
        if (self.start_time is not None) and (self.stop_time is not None):
            return self.start_time <= time <= self.stop_time
        return False

    def apply(self, *args, **kwargs):
        """Applies fault to sensor reading"""
        pass

    @staticmethod
    def validate_inputs(fault_probability, start_time, stop_time):
        """Validate inputs for Fault class and subclasses"""

        # time-based and probability-based faults are mutually exclusive
        if (fault_probability is None) and ((start_time is None) or (stop_time is None)):
            raise ValueError("Time-based fault requires `start_time` and `stop_time` but not `fault_probability`")
        if (fault_probability is not None) and ((start_time is not None) or (stop_time is not None)):
            raise ValueError("Probability-based fault requires `fault_probability` but not `start_time` or `stop_time`")

        # probability must be between 0 and 1
        if fault_probability is not None:
            if not (0 <= fault_probability <= 1):
                raise ValueError("Fault probability must be between 0 and 1")

        # start_time must be less than stop_time
        if (start_time is not None) and (stop_time is not None):
            if not (start_time < stop_time):
                raise ValueError("Fault start_time must be less than stop_time")


class Offset(Fault):
    """Offset fault models a constant offset in the sensor readings.

    Offset or bias fault occurs when a sensor consistently reports values
    that are higher or lower than the true values. This is modeled by
    adding a constant offset to the sensor readings.

    Args:
        offset (float): Offset value.
    """

    def __init__(self, offset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.offset = offset

    def apply(self, time, value):
        """Applies offset fault to sensor reading"""
        if self.is_active(time):
            return value + self.offset
        return value


class Scaling(Fault):
    """Scaling fault occurs when a sensor reports values that are scaled by a factor.

    Scaling or gain fault changes the sensitivity of the sensor,
    causing it to report values that are scaled by a factor.
    This is modeled by multiplying the sensor readings by a scaling factor.

    Args:
        scale (float): Scaling factor.
    """

    def __init__(self, scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = scale

    def apply(self, time, value):
        """Applies scaling fault to sensor reading"""
        if self.is_active(time):
            return value * self.scale
        return value


class Drift(Fault):
    """Drift fault occurs when a sensor values change over time.
    This is modeled by adding a linear drift to the sensor readings.
    The expected behavior for t > stop_time is to return the true value.

    Args:
        rate (float): Drift rate in units of value per second.
    """

    def __init__(self, rate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rate = rate

    def apply(self, time, value):
        """Applies drift fault to sensor reading over time"""
        if self.is_active(time):
            return value + self.rate * (time - self.start_time)
        return value


class StuckAt(Fault):
    """Stuck-at fault occurs when a sensor reports the same value, regardless of the true value.
    This is modeled by replacing the sensor readings with a constant value.

    Args:
        value (float): Stuck-at value.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def apply(self, time, value):
        """Applies stuck-at fault to sensor reading"""
        if self.is_active(time):
            return self.value
        return value
