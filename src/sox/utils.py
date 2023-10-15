from typing import Callable

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter


def derivative_interp1d(x, y, deriv=1, window_length=5, polyorder=2, delta_x=None):
    if delta_x is None:
        assert np.unique(np.gradient(x)).size == 1, "x must be evenly spaced"
        delta_x = x[1] - x[0]

    smoothed_y = savgol_filter(y, window_length, polyorder, deriv=0)
    dy = savgol_filter(smoothed_y, window_length, polyorder, deriv=deriv, delta=delta_x)
    return interp1d(x, dy, kind="linear", fill_value="extrapolate")
