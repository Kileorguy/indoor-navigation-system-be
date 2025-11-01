import numpy as np
from filterpy.kalman import UnscentedKalmanFilter, MerweScaledSigmaPoints
from config import calculate_config

class RSSITrilaterationUKFSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, dt=2):
        if self._initialized:
            return

        self._initialized = True
        self._create_filter(dt)

    def _create_filter(self, dt):
        self.beacons = np.array([calculate_config.BEACON1_POS, calculate_config.BEACON2_POS, calculate_config.BEACON3_POS])
        self.RSSI1 = calculate_config.TX_POWER1
        self.RSSI2 = calculate_config.TX_POWER2
        self.RSSI3 = calculate_config.TX_POWER3

        self.n1 = calculate_config.PATH_LOSS_EXPONENT1
        self.n2 = calculate_config.PATH_LOSS_EXPONENT2
        self.n3 = calculate_config.PATH_LOSS_EXPONENT3
        self.dt = dt

        dim_x = 4
        dim_z = len(self.beacons)
        points = MerweScaledSigmaPoints(n=dim_x, alpha=0.05, beta=1.0, kappa=1.0)

        def fx(x, dt_val):
            F = np.array([
                [1, 0, dt_val, 0],
                [0, 1, 0, dt_val],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            return F @ x

        def hx(x):
            pos = x[:2]
            dists = np.linalg.norm(self.beacons - pos, axis=1)
            dists = np.clip(dists, 0.01, None)  # avoid log(0)

            rssi_expected = np.array([
                self.RSSI1 - 10 * self.n1 * np.log10(dists[0]),
                self.RSSI2 - 10 * self.n2 * np.log10(dists[1]),
                self.RSSI3 - 10 * self.n3 * np.log10(dists[2]),
            ])

            return rssi_expected

        self.ukf = UnscentedKalmanFilter(dim_x=dim_x, dim_z=dim_z, dt=dt, fx=fx, hx=hx, points=points)
        self.ukf.x = np.array([0.0, 0.0, 0.05, 0.05])
        self.ukf.P = np.eye(dim_x) * 2
        self.ukf.Q = np.diag([0.001, 0.001, 0.01, 0.01])
        self.ukf.R = np.eye(dim_z) * 4

    def predict(self):
        self.ukf.predict()

    def update(self, rssi_measurements):
        self.ukf.update(np.array(rssi_measurements))

    def get_position(self):
        return self.ukf.x[:2].copy()

    def get_velocity(self):
        return self.ukf.x[2:].copy()

    def reinitialize(self,dt=2):

        self._create_filter(
           self.dt
        )
