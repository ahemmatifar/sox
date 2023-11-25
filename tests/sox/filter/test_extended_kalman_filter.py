import numpy as np
import pytest
from sox.filter import ExtendedKalmanFilter


@pytest.fixture
def ekf_parameters():
    F = np.array([[1, 1], [0, 1]])  # state transition matrix
    B = np.array([[0.5], [1]])  # control input matrix
    Q = np.array([[0.1, 0], [0, 0.1]])  # process noise covariance
    R = np.array([[1], [2]])  # measurement noise covariance
    x0 = np.array([[1], [1]])  # initial state estimate
    P0 = np.array([[1, 0], [0, 1]])  # initial error covariance
    return F, B, Q, R, x0, P0


@pytest.fixture
def ekf(ekf_parameters):
    return ExtendedKalmanFilter(*ekf_parameters)


def hx(state, arg):  # measurement function
    return np.array([[1.1], [0.1]]) + arg


def h_jacobian(state, arg):  # measurement function Jacobian
    return np.array([[1.1, 0.1], [0.1, 1.1]]) + arg


def test_ekf_predict(ekf, ekf_parameters):
    # predict step
    u = np.array([[1]])
    ekf.predict(u)

    # expected values
    F, B, Q, R, x0, P0 = ekf_parameters
    expected_x = F @ x0 + B @ u
    expected_P = F @ P0 @ F.T + Q

    assert np.allclose(ekf.x, expected_x)
    assert np.allclose(ekf.P, expected_P)


def test_ekf_update(ekf, ekf_parameters):
    # update step
    F, B, Q, R, x0, P0 = ekf_parameters
    z = np.array([[1], [0]])  # measurement (2x1)
    ekf.update(z, hx, h_jacobian, R, hx_args=0.1, hj_args=0.2)

    # expected values
    y = z - hx(x0, 0.1)
    H = h_jacobian(x0, 0.2)
    S = H @ P0 @ H.T + R
    K = P0 @ H.T @ np.linalg.inv(S)
    x = x0 + K @ y
    P = (np.eye(2) - K @ H) @ P0

    assert np.allclose(ekf.x, x)
    assert np.allclose(ekf.P, P)
