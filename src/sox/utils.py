import matplotlib.pyplot as plt
import numpy as np

# import plotly.graph_objects as go
# import plotly.io as pio
# from plotly.subplots import make_subplots
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

# pio.templates.default = "simple_white"

colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]


def derivative_interp1d(x, y, deriv=1, window_length=5, polyorder=2, delta_x=None):
    """Calculates the derivative of a function using Savitzky-Golay filter and interpolation."""
    if delta_x is None:
        assert np.unique(np.gradient(x)).size == 1, "x must be evenly spaced"
        delta_x = x[1] - x[0]

    smoothed_y = savgol_filter(y, window_length, polyorder, deriv=0)
    dy = savgol_filter(smoothed_y, window_length, polyorder, deriv=deriv, delta=delta_x)
    return interp1d(x, dy, kind="linear", fill_value="extrapolate")


def quick_plot(time: list, data: list, legends=None, x_labels=None, y_labels=None, titles=None, n_cols=2):
    """Quickly plot a list of data series with Plotly and return a Figure object"""

    # validate input parameters
    if len(time) != 1 and len(time) != len(data):
        raise ValueError("The length of 'time' should be 1 or match the number of subplots.")

    if x_labels is not None:
        if not isinstance(x_labels, str) and len(x_labels) != len(data):
            raise ValueError("The 'x_labels' parameter should be a string or a list with the same length as 'data'.")

    if y_labels is not None:
        if not isinstance(y_labels, str) and len(y_labels) != len(data):
            raise ValueError("The length of 'y_labels' should match the number of subplots.")

    if legends and len(legends) != len(data):
        raise ValueError("The length of 'legend_labels' should match the number of data series.")

    if titles and len(titles) != len(data):
        raise ValueError("The length of 'titles' should match the number of subplots.")

    # create default labels if not provided
    if legends is None:
        legends = ["Series 1"] * len(data)
        for j, series in enumerate(data):
            if isinstance(series, list):
                legends[j] = [f"Series {k + 1}" for k in range(len(series))]

    num_plots = len(data)
    n_rows = (num_plots + n_cols - 1) // n_cols

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows), constrained_layout=True)
    axs = axs.flatten()

    for plot_idx in range(num_plots):
        t = time[0] if len(time) == 1 else time[plot_idx]

        if isinstance(data[plot_idx], list):  # multiple series in one subplot
            for k, series in enumerate(data[plot_idx]):
                axs[plot_idx].plot(t, series, label=legends[plot_idx][k])
            axs[plot_idx].legend(loc="best")
        else:  # single series in one subplot
            axs[plot_idx].plot(t, data[plot_idx], label=legends[plot_idx])

        x_label_text = None
        if isinstance(x_labels, list):
            x_label_text = x_labels[plot_idx]
        elif isinstance(x_labels, str):
            x_label_text = x_labels

        y_label_text = None
        if isinstance(y_labels, list):
            y_label_text = y_labels[plot_idx]
        elif isinstance(y_labels, str):
            y_label_text = y_labels

        if x_label_text:
            axs[plot_idx].set_xlabel(x_label_text)

        if y_label_text:
            axs[plot_idx].set_ylabel(y_label_text)

        axs[plot_idx].set_title(titles[plot_idx])

    plt.show()


def handle_vector(x):
    """Convert a scalar or 1D array or a 2D row vector to 2D column vector."""
    if np.isscalar(x):  # e.g. x = 1
        return np.atleast_2d(x)
    elif x.ndim == 1:  # e.g. x = np.array([1, 2, 3])
        return np.atleast_2d(x).T
    elif x.ndim == 2 and x.shape[0] == 1:  # e.g. x = np.array([[1, 2, 3]])
        return x.T
    else:
        return x


def handle_matrix(x):
    """Convert a scalar or a row vector to diagonal matrix."""
    if np.isscalar(x):  # e.g. x = 1
        return np.atleast_2d(x)
    elif x.ndim == 1:  # e.g. x = np.array([1, 2, 3])
        return np.diag(x)
    else:
        return x
