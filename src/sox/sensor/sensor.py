class Sensor:
    def __init__(self, name, time, data, noise=None, faults=None):
        self.name = name
        self.time = time
        self.data = data
        self.noise = noise
        self.faults = faults
        self.time_iterator = iter(self.time)
        self.data_iterator = iter(self.data)

    def apply_faults(self, time, sensor_value):
        if self.faults is not None:
            for fault in self.faults:
                sensor_value = fault.apply(time, sensor_value)
        return sensor_value

    def apply_noise(self, sensor_value):
        if self.noise is not None:
            sensor_value = self.noise.apply(sensor_value)
        return sensor_value

    def read(self):
        try:
            time = next(self.time_iterator)
            sensor_value = next(self.data_iterator)

            sensor_value = self.apply_faults(time, sensor_value)
            sensor_value = self.apply_noise(sensor_value)
            return sensor_value
        except StopIteration:
            raise IndexError("No more data available from the sensor")
