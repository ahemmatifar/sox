import numpy as np
from scipy.linalg import cholesky


class MerwePoints:
    def __init__(self, n, alpha, beta, kappa, sqrt_method=None):
        self.n = n
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa
        if sqrt_method is None:
            self.sqrt = cholesky
        else:
            self.sqrt = sqrt_method
        self.Wc, self.Wm = self.weights()

    def points(self, x, P):
        if self.n != np.size(x):
            raise ValueError(f"expected size(x) {self.n}, but size is {np.size(x)}")
        n = self.n

        x = np.atleast_2d(x)
        P = np.atleast_2d(P)

        lambda_ = self.alpha**2 * (n + self.kappa) - n
        U = self.sqrt((lambda_ + n) * P)
        sigmas = np.zeros((n, 2 * n + 1))
        xt = x.transpose()
        sigmas[:, 0] = xt
        for k in range(n):
            sigmas[:, k + 1] = xt + U[k]
            sigmas[:, n + k + 1] = xt - U[k]

        return sigmas

    def weights(self):
        n = self.n
        lambda_ = self.alpha**2 * (n + self.kappa) - n

        c = 0.5 / (n + lambda_)
        Wc = c * np.ones(2 * n + 1)
        Wm = c * np.ones(2 * n + 1)
        Wc[0] = lambda_ / (n + lambda_) + (1 - self.alpha**2 + self.beta)
        Wm[0] = lambda_ / (n + lambda_)

        return Wc, Wm


def unscented_transform(sigma_points, Wm, Wc, noise_cov=None):
    mean = (sigma_points @ Wm)[:, np.newaxis]  # shape (n, 1)
    y = sigma_points - mean  # shape (n, 2n+1)
    cov = y @ np.diag(Wc) @ y.T  # shape (n, n)

    if noise_cov is not None:
        cov += noise_cov
    return mean, cov


class UnscentedKalmanFilter:
    def __init__(self, Q, R, fx, hx, x0, P0, sigma_func):
        self.Q = Q  # Process noise covariance, shape (n, n)
        self.R = R  # Measurement noise covariance, shape (k, k)
        self.fx = fx  # State transition function, shape (n, 1)
        self.hx = hx  # Measurement function, shape (k, 1)
        self.x = x0  # Initial state estimate, shape (n, 1)
        self.P = P0  # Initial error covariance, shape (n, n)
        self.sigma_func = sigma_func  # Sigma point generator

        nx = x0.shape[0]
        nz = R.shape[0]
        self.sigmas_f = np.zeros((nx, 2 * nx + 1))  # predicted sigma points
        self.sigmas_h = np.zeros((nz, 2 * nx + 1))  # measurement sigma points
        self.Wm = sigma_func.Wm  # weights for means, shape (2n+1,)
        self.Wc = sigma_func.Wc  # weights for covariance, shape (2n+1,)

    def predict(self, fx, fx_args=()):
        # calculate sigma points for given mean and covariance
        sigmas = self.sigma_func.points(self.x, self.P)  # shape (n, 2n+1)
        self.sigmas_f = np.hstack([fx(s[:, np.newaxis], *fx_args) for s in sigmas.T])

        # and pass sigmas through the unscented transform to compute prior
        self.x, self.P = unscented_transform(self.sigmas_f, self.Wm, self.Wc, self.Q)

        # update sigma points to reflect the new variance of the points
        self.sigmas_f = self.sigma_func.points(self.x, self.P)

    def update(self, z, R=None, hx=None, hx_args=()):
        if R is None:
            R = self.R

        self.sigmas_h = np.hstack([hx(s[:, np.newaxis], *hx_args) for s in self.sigmas_f.T])

        # mean and covariance of prediction passed through unscented transform
        zp, S = unscented_transform(self.sigmas_h, self.Wm, self.Wc, R)
        S_inv = np.linalg.inv(S)

        # compute cross variance of the state and the measurements
        Pxz = np.zeros((self.x.shape[0], z.shape[0]))
        dx = self.sigmas_f - self.x
        dz = self.sigmas_h - zp
        for i in range(self.sigmas_f.shape[1]):
            Pxz += self.Wc[i] * dx[:, i][:, np.newaxis] @ dz[:, i][np.newaxis, :]

        K = Pxz @ S_inv  # Kalman gain
        y = z - zp  # residual

        # update Gaussian state estimate (x, P)
        self.x = self.x + K @ y
        self.P = self.P - K @ S @ K.T
