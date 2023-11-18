import numpy as np
import pytest
from sox.utils import handle_matrix, handle_vector


@pytest.mark.parametrize(
    "raw_input, expected_output",
    [
        (1, np.array([[1]])),  # scalar
        (np.array([1, 2, 3]), np.array([[1], [2], [3]])),  # 1D array
        (np.array([[1, 2, 3]]), np.array([[1], [2], [3]])),  # 2D row vector
        (np.array([[1], [2], [3]]), np.array([[1], [2], [3]])),  # 2D column vector
    ],
)
def test_vector_handling(raw_input, expected_output):
    assert np.array_equal(handle_vector(raw_input), expected_output)


@pytest.mark.parametrize(
    "raw_input, expected_output",
    [
        (1, np.array([[1]])),  # scalar
        (np.array([1, 2, 3]), np.diag([1, 2, 3])),  # 1D array
    ],
)
def test_matrix_handling(raw_input, expected_output):
    assert np.array_equal(handle_matrix(raw_input), expected_output)
