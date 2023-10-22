from typing import Callable

import numpy as np
from scipy.interpolate import interp1d

from sox.utils import derivative_interp1d


class SOCWithEKF:
    def __init__(self, ocv_func: Callable, rc_pairs: int):
        self.ocv = self.build_ocv_func(ocv_func)
        self.docv = self.build_docv_func(ocv_func)
        self.rc_pairs = rc_pairs

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

    def hx(self, x, r0, current):
        """Returns voltage measurement (z=hx)."""
        soc = x[0, 0]
        v_rc = x[1:, 0]
        voltage = self.ocv(soc) - np.sum(v_rc) - r0 * current
        return np.array([[voltage]])

    def h_jacobian(self, x):
        """Returns Jacobian of voltage measurement (H)."""
        soc = x[0, 0]
        jac = [self.docv(soc), *([-1] * self.rc_pairs)]
        return np.array([jac])
