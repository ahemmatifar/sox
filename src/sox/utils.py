import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

pio.templates.default = "simple_white"

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


def quick_plot(time, data: list, legends=None, x_labels=None, y_labels=None, titles=None):
    """Checks if the input parameters have the correct format and lengths."""

    # validate input parameters
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
    n_cols = 2
    n_rows = (num_plots + n_cols - 1) // n_cols

    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=titles)

    for plot_idx in range(num_plots):
        row = plot_idx // n_cols + 1
        col = plot_idx % n_cols + 1

        if isinstance(data[plot_idx], list):
            for k, series in enumerate(data[plot_idx]):
                fig.add_trace(
                    go.Scatter(x=time, y=series, mode="lines", name=legends[plot_idx][k], line=dict(color=colors[k])),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Scatter(x=time, y=data[plot_idx], mode="lines", name=legends[plot_idx], line=dict(color=colors[plot_idx])),
                row=row,
                col=col,
            )

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
            fig.update_xaxes(title_text=x_label_text, showgrid=False, row=row, col=col)

        if y_label_text:
            fig.update_yaxes(title_text=y_label_text, showgrid=False, row=row, col=col)

    fig.update_layout(
        showlegend=True,
        width=1000,
        height=350 * n_rows,
    )
    fig.show()


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
