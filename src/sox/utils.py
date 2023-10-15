import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt


def derivative_interp1d(x, y, deriv=1, window_length=5, polyorder=2, delta_x=None):
    """"""
    if delta_x is None:
        assert np.unique(np.gradient(x)).size == 1, "x must be evenly spaced"
        delta_x = x[1] - x[0]

    smoothed_y = savgol_filter(y, window_length, polyorder, deriv=0)
    dy = savgol_filter(smoothed_y, window_length, polyorder, deriv=deriv, delta=delta_x)
    return interp1d(x, dy, kind="linear", fill_value="extrapolate")


def quick_plot(data, sampling_time: float, legend=None, x_label=None, y_label=None, title=None):
    """Create subplots for multiple time series data with varying x-axes, preset solid lines, a selection of
    colors, and customizable plot updating. Automatically determines the number of rows based on data length."""

    # Check if the input parameters have the correct format and lengths
    if not data:
        raise ValueError("The 'data' parameter is empty. Please provide time series data.")

    if x_label and (not isinstance(x_label, str) and len(x_label) != len(data)):
        raise ValueError("The 'x_labels' parameter should be a string or a list with the same length as 'data'.")

    if legend and len(legend) != len(data):
        raise ValueError("The length of 'legend_labels' should match the number of data series.")

    if title and len(title) != len(data):
        raise ValueError("The length of 'titles' should match the number of subplots.")

    if y_label and (not isinstance(y_label, str) and len(y_label) != len(data)):
        raise ValueError("The length of 'y_labels' should match the number of subplots.")

    if legend is None:
        legend = ["Series 1"] * len(data)
        for j, series in enumerate(data):
            if isinstance(series, list):
                legend[j] = [f"Series {k + 1}" for k in range(len(series))]

    # n_time = 0
    # if isinstance(data[0][0], list):
    # time = [sampling_time * i for i in range(n_time)]  # shared time axis for all subplots

    # Best set of colors
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

    num_plots = len(data)
    n_cols = 2  # number of columns
    n = (num_plots + n_cols - 1) // n_cols  # number of rows
    fig, axes = plt.subplots(n, 2, figsize=(10, 3 * n))

    for idx in range(num_plots):
        ax = axes[idx // n_cols][idx % n_cols]

        if title and idx < len(title):
            ax.set_title(title[idx])

        if isinstance(x_label, str):
            ax.set_xlabel(x_label)  # Use a single x-axis label for all subplots
        elif x_label and idx < len(x_label):
            ax.set_xlabel(x_label[idx])  # Use the corresponding x-axis label for each subplot

        if isinstance(y_label, str):
            ax.set_ylabel(y_label)
        elif y_label and idx < len(y_label):
            ax.set_ylabel(y_label[idx])

        if isinstance(data[idx], list):
            for k, series in enumerate(data[idx]):
                time = [sampling_time * i for i in range(len(series))]
                ax.plot(time, series, color=colors[k], label=legend[idx][k])
        else:
            time = [sampling_time * i for i in range(len(data[idx]))]
            ax.plot(time, data[idx], color=colors[idx], label=legend[idx])

    # apply to all subplots
    for ax in fig.axes:
        ax.grid(False)
        ax.legend(loc='best')  # Use a tight legend placement

    plt.tight_layout()
    plt.show()

    return fig, axes  # Return figure and axes objects for further customization
