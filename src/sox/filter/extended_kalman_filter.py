import numpy as np

from sox.utils import handle_matrix, handle_vector


class ExtendedKalmanFilter:
    """Extended Kalman Filter (EKF)

    Args:
        F (array_like): State transition matrix, shape (n, n)
        B (array_like): Control input matrix, shape (n, m)
        Q (array_like): Process noise covariance, shape (n, n)
        R (array_like): Measurement noise covariance, shape (k, k)
        x0 (array_like): Initial state estimate, shape (n, 1)
        P0 (array_like): Initial error covariance, shape (n, n)

    Attributes:
        F (array_like): State transition matrix, shape (n, n)
        B (array_like): Control input matrix, shape (n, m)
        Q (array_like): Process noise covariance, shape (n, n)
        R (array_like): Measurement noise covariance, shape (k, k)
        x (array_like): Current state estimate, shape (n, 1)
        P (array_like): Current error covariance, shape (n, n)
        x0 (array_like): Initial state estimate, shape (n, 1)
        P0 (array_like): Initial error covariance, shape (n, n)
        I (array_like): Identity matrix, shape (n, n)
    """

    def __init__(self, F, B, Q, R, x0, P0):
        self.F = handle_matrix(F)  # State transition matrix
        self.B = handle_matrix(B)  # Control input matrix
        self.Q = handle_matrix(Q)  # Process noise covariance
        self.R = handle_matrix(R)  # Measurement noise covariance
        self.x = handle_vector(x0)  # Initial state estimate
        self.P = handle_matrix(P0)  # Initial error covariance
        self.x0 = handle_vector(x0)  # Initial state estimate
        self.P0 = handle_matrix(P0)  # Initial error covariance

        self.I = np.eye(F.shape[0])  # Identity matrix

    def predict(self, u):
        """Predicts the next state estimate based on control input u

        Args:
            u (array_like): Control input, shape (m, 1)
        """
        u = handle_vector(u)

        self.x = self.F @ self.x + self.B @ u
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z, hx, h_jacobian, R=None, hx_args=(), hj_args=()):
        """Updates the state estimate based on measurement z

        Args:
            z (array_like): Measurement, shape (k, 1)
            hx (callable): Measurement function, shape (n, 1) -> (k, 1)
            h_jacobian (callable): Measurement Jacobian function, shape (k, n) -> (k, n)
            R (array_like, optional): Measurement noise covariance, shape (k, k)
            hx_args (tuple, optional): Additional arguments to pass to Hx
            hj_args (tuple, optional): Additional arguments to pass to h_jacobian

        Raises:
            ValueError: If z, hx, or h_jacobian have invalid shapes
        """
        z = handle_vector(z)

        if not isinstance(hx_args, tuple):
            hx_args = (hx_args,)
        if not isinstance(hj_args, tuple):
            hj_args = (hj_args,)
        if R is None:
            R = self.R

        y = z - hx(self.x, *hx_args)
        H = h_jacobian(self.x, *hj_args)
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (self.I - K @ H) @ self.P

    def reset(self):
        """Resets the state estimate and error covariance to their initial values"""
        self.x = self.x0
        self.P = self.P0
