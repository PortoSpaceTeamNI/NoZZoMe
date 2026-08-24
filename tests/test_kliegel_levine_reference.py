"""Regression checks against the published third-order Kliegel--Levine series."""

import math
import unittest

import numpy as np

from method_of_caracteristics.initial_transient_line import (
    _kliegel_levine_velocity_ratios,
    kliegel_levine_discharge_coefficient,
)


def _published_velocity_ratios(x, y, gamma, curvature):
    """Independent implementation of Hall/Kliegel--Levine's uniform-flow series."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    lam = curvature + 1.0
    z = x * np.sqrt(2.0 * curvature / (gamma + 1.0))

    u1 = y**2 / 2.0 - 1.0 / 4.0 + z
    v1 = y**3 / 4.0 - y / 4.0 + y * z
    u2 = (
        (2.0 * gamma + 9.0) * y**4 / 24.0
        - (4.0 * gamma + 15.0) * y**2 / 24.0
        + (10.0 * gamma + 57.0) / 288.0
        + z * (y**2 - 5.0 / 8.0)
        - (2.0 * gamma - 3.0) * z**2 / 6.0
    )
    v2 = (
        (gamma + 3.0) * y**5 / 9.0
        - (20.0 * gamma + 63.0) * y**3 / 96.0
        + (28.0 * gamma + 93.0) * y / 288.0
        + z
        * (
            (2.0 * gamma + 9.0) * y**3 / 6.0
            - (4.0 * gamma + 15.0) * y / 12.0
        )
        + y * z**2
    )
    u3 = (
        (556.0 * gamma**2 + 1737.0 * gamma + 3069.0) * y**6 / 10368.0
        - (388.0 * gamma**2 + 1161.0 * gamma + 1881.0) * y**4 / 2304.0
        + (304.0 * gamma**2 + 831.0 * gamma + 1242.0) * y**2 / 1728.0
        - (2708.0 * gamma**2 + 7839.0 * gamma + 14211.0) / 82944.0
        + z
        * (
            (52.0 * gamma**2 + 51.0 * gamma + 327.0) * y**4 / 384.0
            - (52.0 * gamma**2 + 75.0 * gamma + 279.0) * y**2 / 192.0
            + (92.0 * gamma**2 + 180.0 * gamma + 639.0) / 1152.0
        )
        + z**2
        * (-(7.0 * gamma - 3.0) * y**2 / 8.0 + (13.0 * gamma - 27.0) / 48.0)
        + (4.0 * gamma**2 - 57.0 * gamma + 27.0) * z**3 / 144.0
    )
    v3 = (
        (6836.0 * gamma**2 + 23031.0 * gamma + 30627.0) * y**7 / 82944.0
        - (3380.0 * gamma**2 + 11391.0 * gamma + 15291.0) * y**5 / 13824.0
        + (3424.0 * gamma**2 + 11271.0 * gamma + 15228.0) * y**3 / 13824.0
        - (7100.0 * gamma**2 + 22311.0 * gamma + 30249.0) * y / 82944.0
        + z
        * (
            (556.0 * gamma**2 + 1737.0 * gamma + 3069.0) * y**5 / 1728.0
            - (388.0 * gamma**2 + 1161.0 * gamma + 1881.0) * y**3 / 576.0
            + (304.0 * gamma**2 + 831.0 * gamma + 1242.0) * y / 864.0
        )
        + z**2
        * (
            (52.0 * gamma**2 + 51.0 * gamma + 327.0) * y**3 / 192.0
            - (52.0 * gamma**2 + 75.0 * gamma + 279.0) * y / 192.0
        )
        - (7.0 * gamma - 3.0) * y * z**3 / 12.0
    )

    axial = 1.0 + u1 / lam + (u1 + u2) / lam**2 + (u1 + 2.0 * u2 + u3) / lam**3
    radial = math.sqrt((gamma + 1.0) / (2.0 * lam)) * (
        v1 / lam
        + (1.5 * v1 + v2) / lam**2
        + (15.0 * v1 / 8.0 + 2.5 * v2 + v3) / lam**3
    )
    return axial, radial


class KliegelLevinePublishedSeriesTests(unittest.TestCase):
    def test_all_velocity_terms_match_published_uniform_flow_series(self):
        x = np.array([-0.08, 0.0, 0.11, 0.23])
        y = np.array([0.0, 0.27, 0.63, 1.0])
        for gamma in (1.12, 1.1668320362434539, 1.4):
            for curvature in (0.625, 1.5, 4.0):
                expected = _published_velocity_ratios(x, y, gamma, curvature)
                actual = _kliegel_levine_velocity_ratios(x, y, gamma, curvature)
                np.testing.assert_allclose(actual[0], expected[0], rtol=2e-15, atol=2e-15)
                np.testing.assert_allclose(actual[1], expected[1], rtol=2e-15, atol=2e-15)

    def test_throat_wall_radial_velocity_is_zero(self):
        for gamma in (1.12, 1.2, 1.4):
            for curvature in (0.625, 1.5, 4.0):
                _, radial = _kliegel_levine_velocity_ratios(
                    0.0, 1.0, gamma, curvature
                )
                self.assertAlmostEqual(float(radial), 0.0, places=14)

    def test_discharge_coefficient_matches_published_third_order_expression(self):
        for gamma, curvature in ((1.12, 0.625), (1.2, 1.5), (1.4, 4.0)):
            lam = 1.0 + curvature
            expected = 1.0 - (gamma + 1.0) / lam**2 * (
                1.0 / 96.0
                - (8.0 * gamma - 27.0) / (2304.0 * lam)
                + (754.0 * gamma**2 - 757.0 * gamma + 3633.0)
                / (276480.0 * lam**2)
            )
            self.assertAlmostEqual(
                kliegel_levine_discharge_coefficient(gamma, curvature),
                expected,
                places=15,
            )


if __name__ == "__main__":
    unittest.main()
