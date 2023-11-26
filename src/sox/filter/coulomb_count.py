class CoulombCount:
    """Coulomb counting for estimating the state of charge (SOC) of a battery.

    Args:
        initial_soc (float): Initial state of charge (SOC) of the battery.
        capacity (float): Capacity of the battery in Ah.
        sampling_time (float): Sampling time in seconds.

    Attributes:
        initial_soc (float): Initial state of charge (SOC) of the battery.
        capacity (float): Capacity of the battery in Ah.
        sampling_time (float): Sampling time in seconds.
        soc (float): Current state of charge (SOC) of the battery.
    """

    def __init__(self, initial_soc: float, capacity: float, sampling_time: float):
        self.initial_soc = initial_soc
        self.capacity = capacity  # Ah
        self.sampling_time = sampling_time  # s
        self.soc = initial_soc

    def predict(self, current: float):
        """Predicts the state of charge (SOC) of the battery.

        Args:
            current (float): Current of the battery in A.
        """
        self.soc -= current * self.sampling_time / (self.capacity * 3600)

    def reset(self):
        """Resets the state of charge (SOC) of the battery."""
        self.soc = self.initial_soc


class CoulombCountVariableCapacity:
    """Coulomb counting for estimating the state of charge (SOC) of a battery.

    Args:
        initial_soc (float): Initial state of charge (SOC) of the battery.
        sampling_time (float): Sampling time in seconds.

    Attributes:
        initial_soc (float): Initial state of charge (SOC) of the battery.
        sampling_time (float): Sampling time in seconds.
        soc (float): Current state of charge (SOC) of the battery.
    """

    def __init__(
        self,
        initial_soc: float,
        sampling_time: float,
    ):
        self.initial_soc = initial_soc
        self.sampling_time = sampling_time  # s
        self.soc = initial_soc

    def predict(self, current: float, capacity: float):
        """Predicts the state of charge (SOC) of the battery.

        Args:
            current (float): Current of the battery in A.
            capacity (float): Capacity of the battery in Ah.
        """
        self.soc -= current * self.sampling_time / (capacity * 3600)

    def reset(self):
        """Resets the state of charge (SOC) of the battery."""
        self.soc = self.initial_soc
