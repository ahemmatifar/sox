import numpy as np
from scipy.linalg import cholesky

from sox.utils import handle_matrix, handle_vector


class MerweSigmaPoints:
    """Sigma points for Unscented Kalman Filter

    Parameters and Attributes
    ----------
    n : int
        Dimensionality of the state. 2n+1 weights will be generated.
    alpha : float
        Spread of the sigma points around the mean. Typically, 1e-3.
    beta : float
        Used to incorporate prior knowledge of the distribution of the mean.
        For Gaussian x, beta=2 is optimal, and corresponds to 95% confidence.
    kappa : float
        Secondary scaling parameter usually set to 0 or 3-n.
    sqrt_method : callable
        Function that computes the square root of a matrix. Defaults to scipy.linalg.cholesky.
    """

    def __init__(self, n: int, alpha: float, beta: float, kappa: float, sqrt_method=None):
        self.n = n
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa
        if sqrt_method is None:
            self.sqrt = cholesky
        else:
            self.sqrt = sqrt_method
        self.wm, self.wc = self.weights()

    def points(self, x, P):
        """Generate sigma points for given mean and covariance

        Parameters
        ----------
        x : array_like
            Mean vector, shape (n, 1)
        P : array_like
            Covariance matrix, shape (n, n)

        Returns
        -------
        sigmas : array_like
            Sigma points, shape (n, 2n+1)
        """
        n = self.n
        if n != x.shape[0] or (n, n) != P.shape:
            raise ValueError(
                f"Expected x.shape = ({n}, 1) and P.shape = ({n}, {n}). "
                f"Got x.shape = {x.shape} and P.shape = {P.shape} instead."
            )

        lambda_ = self.alpha**2 * (n + self.kappa) - n
        delta = self.sqrt((lambda_ + n) * P)
        sigma_points = np.zeros((n, 2 * n + 1))
        xt = x.transpose()
        sigma_points[:, 0] = xt
        for k in range(n):
            sigma_points[:, k + 1] = xt + delta[k]
            sigma_points[:, n + k + 1] = xt - delta[k]
        return sigma_points

    def weights(self):
        """Compute weights for mean and covariance

        Returns
        -------
        mean_weights : array_like
            Weights for mean, shape (2n+1,)
        cov_weights : array_like
            Weights for covariance, shape (2n+1,)
        """
        n = self.n
        lambda_ = self.alpha**2 * (n + self.kappa) - n
        c = 0.5 / (n + lambda_)

        mean_weights = c * np.ones(2 * n + 1)
        mean_weights[0] = lambda_ / (n + lambda_)

        cov_weights = c * np.ones(2 * n + 1)
        cov_weights[0] = lambda_ / (n + lambda_) + (1 - self.alpha**2 + self.beta)

        return mean_weights, cov_weights


def unscented_transform(sigma_points, wm, wc, noise_cov=None):
    """Unscented transform

    Parameters
    ----------
    sigma_points : array_like
        Sigma points, shape (n, 2n+1)
    wm : array_like
        Weights for mean, shape (2n+1,)
    wc : array_like
        Weights for covariance, shape (2n+1,)
    noise_cov : array_like, optional
        Covariance matrix for additive noise, shape (n, n)
    """
    mean = (sigma_points @ wm)[:, np.newaxis]  # shape (n, 1)
    y = sigma_points - mean  # shape (n, 2n+1)
    cov = y @ np.diag(wc) @ y.T  # shape (n, n)
    if noise_cov is not None:
        cov += noise_cov
    return mean, cov


class UnscentedKalmanFilter:
    """Unscented Kalman Filter

    Parameters and Attributes
    ----------
    Q : array_like
        Process noise covariance, shape (n, n)
    R : array_like
        Measurement noise covariance, shape (k, k)
    x0 : array_like
        Initial state estimate, shape (n, 1)
    P0 : array_like
        Initial error covariance, shape (n, n)
    sigma_gen : callable
        Sigma point generator
    sigmas_f : array_like
        Predicted sigma points, shape (n, 2n+1)
    sigmas_h : array_like
        Measurement sigma points, shape (k, 2n+1)
    wm : array_like
        Weights for means, shape (2n+1,)
    wc : array_like
        Weights for covariance, shape (2n+1,)
    """

    def __init__(self, Q, R, x0, P0, sigma_gen):
        self.Q = handle_matrix(Q)  # Process noise covariance, shape (n, n)
        self.R = handle_matrix(R)  # Measurement noise covariance, shape (k, k)
        self.x = handle_vector(x0)  # Initial state estimate, shape (n, 1)
        self.P = handle_matrix(P0)  # Initial error covariance, shape (n, n)
        self.x0 = handle_vector(x0)
        self.P0 = handle_matrix(P0)

        self.sigma_gen = sigma_gen  # Sigma point generator
        self.nx = self.x0.shape[0]
        self.nz = self.R.shape[0]
        self.sigmas_f = np.zeros((self.nx, 2 * self.nx + 1))  # predicted sigma points
        self.sigmas_h = np.zeros((self.nz, 2 * self.nx + 1))  # measurement sigma points
        self.wm = sigma_gen.wm  # weights for means, shape (2n+1,)
        self.wc = sigma_gen.wc  # weights for covariance, shape (2n+1,)

    def predict(self, fx, fx_args=()):
        """Predict step of the filter

        Parameters
        ----------
        fx : callable
            State transition function, shape (n, 1) -> (n, 1)
        fx_args : tuple, optional
            Additional arguments to pass to fx
        """
        if not isinstance(fx_args, tuple):
            fx_args = (fx_args,)

        # calculate sigma points for given mean and covariance
        sigmas = self.sigma_gen.points(self.x, self.P)  # shape (n, 2n+1)
        self.sigmas_f = np.hstack([fx(s[:, np.newaxis], *fx_args) for s in sigmas.T])

        # pass sigmas through the unscented transform to compute prior
        self.x, self.P = unscented_transform(self.sigmas_f, self.wm, self.wc, self.Q)

        # update sigma points to reflect the new variance of the points
        self.sigmas_f = self.sigma_gen.points(self.x, self.P)

    def update(self, z, hx, R=None, hx_args=()):
        """Update step of the filter

        Parameters
        ----------
        z : array_like
            Measurement vector, shape (k, 1)
        hx : callable
            Measurement function, shape (n, 1) -> (k, 1)
        R : array_like, optional
            Measurement noise covariance, shape (k, k)
        hx_args : tuple, optional
            Additional arguments to pass to hx
        """
        z = handle_vector(z)

        if not isinstance(hx_args, tuple):
            hx_args = (hx_args,)
        if R is None:
            R = self.R

        self.sigmas_h = np.hstack([hx(s[:, np.newaxis], *hx_args) for s in self.sigmas_f.T])

        # mean and covariance of prediction passed through unscented transform
        zp, S = unscented_transform(self.sigmas_h, self.wm, self.wc, R)

        # compute cross variance of the state and the measurements
        Pxz = np.zeros((self.nx, self.nz))
        dx = self.sigmas_f - self.x
        dz = self.sigmas_h - zp
        for i in range(self.sigmas_f.shape[1]):
            Pxz += self.wc[i] * dx[:, i][:, np.newaxis] @ dz[:, i][np.newaxis, :]

        K = Pxz @ np.linalg.inv(S)  # Kalman gain
        y = z - zp  # residual

        # update Gaussian state estimate (x, P)
        self.x = self.x + K @ y
        self.P = self.P - K @ S @ K.T

    def reset(self):
        """Reset the filter to its initial state"""
        self.x = self.x0
        self.P = self.P0
        self.sigmas_f = self.sigma_gen.points(self.x, self.P)
        self.sigmas_h = np.zeros((self.nz, 2 * self.nx + 1))
        self.wm = self.sigma_gen.wm
        self.wc = self.sigma_gen.wc
