import numpy as np


class Noise:
    def apply(self, value):
        pass


class Uniform(Noise):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def apply(self, value):
        noise = np.random.uniform(self.min_value, self.max_value)
        return value + noise


class Normal(Noise):
    def __init__(self, mean, std_dev):
        self.mean = mean
        self.std_dev = std_dev

    def apply(self, value):
        noise = np.random.normal(self.mean, self.std_dev)
        return value + noise


class Poisson(Noise):
    def __init__(self, lam):
        self.lam = lam  # Lambda parameter for Poisson distribution

    def apply(self, value):
        noise = np.random.poisson(self.lam)
        return value + noise


class Exponential(Noise):
    def __init__(self, scale):
        self.scale = scale  # Scale parameter for exponential distribution

    def apply(self, value):
        noise = np.random.exponential(self.scale)
        return value + noise