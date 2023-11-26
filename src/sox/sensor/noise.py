import numpy as np


class Noise:
    """Base class for sensor noise

    Args:
        random_seed (int): Random seed for reproducibility.
    """

    def __init__(self, random_seed=None):
        if random_seed is not None:
            np.random.seed(random_seed)

    def apply(self, value):
        """Applies noise to sensor reading"""
        pass


class Uniform(Noise):
    """Uniform noise

    Args:
        min_value (float): Minimum value of noise.
        max_value (float): Maximum value of noise.
    """

    def __init__(self, min_value, max_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def apply(self, value):
        """Applies uniform noise to sensor reading"""
        noise = np.random.uniform(self.min_value, self.max_value)
        return value + noise


class Normal(Noise):
    """Normal noise

    Args:
        mean (float): Mean of noise.
        std_dev (float): Standard deviation of noise.
    """

    def __init__(self, mean, std_dev, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mean = mean
        self.std_dev = std_dev

    def apply(self, value):
        """Applies normal noise to sensor reading"""
        noise = np.random.normal(self.mean, self.std_dev)
        return value + noise


class Poisson(Noise):
    """Poisson noise

    Args:
        lam (float): Lambda parameter for Poisson distribution.
    """

    def __init__(self, lam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lam = lam  # Lambda parameter for Poisson distribution

    def apply(self, value):
        """Applies Poisson noise to sensor reading"""
        noise = np.random.poisson(self.lam)
        return value + noise


class Exponential(Noise):
    """Exponential noise

    Args:
        scale (float): Scale parameter for exponential distribution.
    """

    def __init__(self, scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = scale  # Scale parameter for exponential distribution

    def apply(self, value):
        """Applies exponential noise to sensor reading"""
        noise = np.random.exponential(self.scale)
        return value + noise
