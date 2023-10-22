from typing import Callable, List

import numpy as np
from scipy.interpolate import interp1d


class SOCWithUKF:
    def __init__(self, ocv_func: Callable, rc_resistances: List[float], rc_capacitors: List[float], capacity: float):
        self.ocv = self.build_ocv_func(ocv_func)
        self.rc_resistances = rc_resistances
        self.rc_capacitors = rc_capacitors
        self.capacity = capacity
        assert len(rc_resistances) == len(rc_capacitors)

    @staticmethod
    def build_ocv_func(ocv_func):
        delta_soc = 0.001
        soc = np.arange(0, 1 + delta_soc, delta_soc)
        ocv = [ocv_func([s]).evaluate()[0, 0] for s in soc]  # evaluates pb.Interpolant
        return interp1d(soc, ocv, kind="linear", fill_value="extrapolate")

    def hx(self, x, r0: float, current: float):
        """Returns voltage measurement (z=Hx)."""
        soc = x[0, 0]
        v_rc = x[1:, 0]
        voltage = self.ocv(soc) - np.sum(v_rc) - r0 * current
        return np.array([[voltage]])

    def fx(self, x, current: float, dt: float):
        """State transition function"""
        soc = x[0, 0]
        v_rc = x[1:, 0]
        soc_new = soc - current / self.capacity
        v_rc_new = [
            v * np.exp(-dt / (r * c)) + current * r * (1 - np.exp(-dt / (r * c)))
            for v, r, c in zip(v_rc, self.rc_resistances, self.rc_capacitors)
        ]
        return np.array([soc_new, *v_rc_new])[:, np.newaxis]
