import numpy as np


class ExtendedKalmanFilter:
    """Extended Kalman Filter

    Parameters and Attributes
    ----------
    F : array_like
        State transition matrix
    B : array_like
        Control input matrix
    Q : array_like
        Process noise covariance
    R : array_like
        Measurement noise covariance
    x0 : array_like
        Initial state estimate
    P0 : array_like
        Initial error covariance
    P : array_like
        Initial error covariance
    """

    def __init__(self, F, B, Q, R, x0, P0):
        self.F = F  # State transition matrix
        self.B = B  # Control input matrix
        self.Q = Q  # Process noise covariance
        self.R = R  # Measurement noise covariance
        self.x = x0  # Initial state estimate
        self.P = P0  # Initial error covariance
        self.I = np.eye(F.shape[0])  # Identity matrix

    def predict(self, u):
        """Predict next state

        Parameters
        ----------
        u : array_like
            Control input, shape (m, 1)
        """
        self.x = self.F @ self.x + self.B @ u
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z, hx, h_jacobian, R=None, hx_args=(), hj_args=()):
        """Update state estimate based on measurement z

        Parameters
        ----------
        z : array_like
            Measurement, shape (k, 1)
        hx : callable
            Measurement function, shape (n, 1) -> (k, 1)
        h_jacobian : callable
            Measurement Jacobian function, shape (k, n) -> (k, n)
        R : array_like, optional
            Measurement noise covariance, shape (k, k)
        hx_args : tuple, optional
            Additional arguments to pass to Hx
        hj_args : tuple, optional
            Additional arguments to pass to h_jacobian
        """
        if R is None:
            R = self.R

        y = z - hx(self.x, *hx_args)
        H = h_jacobian(self.x, *hj_args)
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y

        # P = (I-KH)P(I-KH)' + KRK' is more numerically stable
        # P = (I-KH)P usually seen in the literature.
        # self.P = (1 - K @ H) @ self.P
        I_KH = self.I - K @ H
        self.P = I_KH @ self.P @ I_KH.T + K @ R @ K.T
