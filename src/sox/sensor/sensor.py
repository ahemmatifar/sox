class Sensor:
    """Sensor class that reads data from a file and applies noise and faults.

    Args:
        name (str): Name of sensor.
        time (array-like): List of times in seconds.
        data (array-like): List of sensor data.
        noise (Noise): Noise object.
        faults (list): List of Fault objects.
    """

    def __init__(self, name, time, data, noise=None, faults=None):
        self.name = name
        self.time = time
        self.data = data
        self.noise = noise
        self.faults = faults
        self.time_iterator = iter(self.time)
        self.data_iterator = iter(self.data)

    def apply_faults(self, time, sensor_value):
        """Applies faults to sensor reading at given time

        Args:
            time (float): Time in seconds.
            sensor_value (float): Sensor reading.
        Returns:
            float: Sensor reading with faults applied.
        """
        if self.faults is not None:
            for fault in self.faults:
                sensor_value = fault.apply(time, sensor_value)
        return sensor_value

    def apply_noise(self, sensor_value):
        """Applies noise to sensor reading"""
        if self.noise is not None:
            sensor_value = self.noise.apply(sensor_value)
        return sensor_value

    def read(self):
        """Reads sensor value at next time step and applies noise and faults to it

        Returns:
            float: Sensor reading with noise and faults applied.
        """
        try:
            time = next(self.time_iterator)
            sensor_value = next(self.data_iterator)
            sensor_value = self.apply_faults(time, sensor_value)
            sensor_value = self.apply_noise(sensor_value)
            return sensor_value
        except StopIteration:
            raise IndexError(f"Sensor '{self.name}' finished reading.")

    def reset(self):
        """Resets sensor to beginning of data set"""
        self.time_iterator = iter(self.time)
        self.data_iterator = iter(self.data)
