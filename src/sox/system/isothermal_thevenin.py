from typing import Callable, List

import numpy as np
from scipy.interpolate import interp1d

from sox.utils import derivative_interp1d


class IsothermalThevenin:
    def __init__(
        self,
        ocv_func: Callable,
        series_resistance: float,
        rc_resistors: List[float],
        rc_capacitors: List[float],
        capacity: float,
    ):
        self.ocv = self.build_ocv_func(ocv_func)
        self.docv = self.build_docv_func(ocv_func)
        self.series_resistance = series_resistance
        self.rc_resistances = rc_resistors
        self.rc_capacitors = rc_capacitors
        self.capacity = capacity
        assert len(rc_resistors) == len(rc_capacitors)

    @staticmethod
    def build_ocv_func(ocv_func):
        delta_soc = 0.001
        soc = np.arange(0, 1 + delta_soc, delta_soc)
        ocv = [ocv_func([s]).evaluate()[0, 0] for s in soc]  # evaluates pb.Interpolant
        return interp1d(soc, ocv, kind="linear", fill_value="extrapolate")

    @staticmethod
    def build_docv_func(ocv_func):
        """Returns the derivative of the open-circuit voltage with respect to state of charge."""
        delta_soc = 0.001
        soc = np.arange(0, 1 + delta_soc, delta_soc)
        ocv = [ocv_func([s]).evaluate()[0, 0] for s in soc]  # evaluates pb.Interpolant
        return derivative_interp1d(soc, ocv, delta_x=delta_soc)

    def F(self, dt: float):
        """State transition matrix"""
        f = [np.exp(-dt / (r * c)) for r, c in zip(self.rc_resistances, self.rc_capacitors)]
        f = [1, *f]
        return np.diag(f)

    def B(self, dt: float):
        """Input matrix"""
        b1 = -dt / (self.capacity * 3600.0)
        b2 = [r * (1 - np.exp(-dt / (r * c))) for r, c in zip(self.rc_resistances, self.rc_capacitors)]
        b = [b1, *b2]
        return np.array(b)[:, np.newaxis]

    def fx(self, x, current: float, dt: float):
        """State transition function"""
        soc = x[0, 0]
        v_rc = x[1:, 0]
        soc_new = soc - current / (self.capacity * 3600.0)
        v_rc_new = [
            v * np.exp(-dt / (r * c)) + current * r * (1 - np.exp(-dt / (r * c)))
            for v, r, c in zip(v_rc, self.rc_resistances, self.rc_capacitors)
        ]
        return np.array([soc_new, *v_rc_new])[:, np.newaxis]

    def hx(self, x, current):
        """Returns voltage measurement"""
        soc = x[0, 0]
        v_rc = x[1:, 0]
        voltage = self.ocv(soc) - np.sum(v_rc) - self.series_resistance * current
        return np.array([[voltage]])

    def h_jacobian(self, x):
        """Returns Jacobian of voltage measurement"""
        soc = x[0, 0]
        jac1 = self.docv(soc)
        jac2 = [-1] * len(self.rc_resistances)
        jac = [jac1, *jac2]
        return np.array([jac])
