class CoulombCount:
    def __init__(self, initial_soc: float, capacity: float, sampling_time: float):
        self.initial_soc = initial_soc
        self.capacity = capacity  # Ah
        self.sampling_time = sampling_time  # s
        self.soc = initial_soc

    def update(self, current):
        self.soc -= current * self.sampling_time / (self.capacity * 3600)
        return self.soc


class CoulombCountVariableCapacity:
    def __init__(
        self,
        initial_soc: float,
        sampling_time: float,
    ):
        self.initial_soc = initial_soc
        self.sampling_time = sampling_time  # s
        self.soc = initial_soc

    def update(self, current, capacity):
        self.soc -= current * self.sampling_time / (capacity * 3600)
        return self.soc
