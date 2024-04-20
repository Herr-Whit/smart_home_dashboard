from unittest import TestCase

from src.dashboard_builder import SimpleDashboardBuilder
from src.models.dashboard_input import DashboardInput


class TestSimpleDashboardBuilder(TestCase):
    def test_build_dashboard(self):
        test_data = {
            "current": {
                "total": 0.2634,
                "energy": 0.0628,
                "tax": 0.2006,
                "startsAt": "2024-04-20T17:00:00.000+02:00",
            },
            "today": [
                {
                    "total": 0.2603,
                    "energy": 0.0602,
                    "tax": 0.2001,
                    "startsAt": "2024-04-20T00:00:00.000+02:00",
                },
                {
                    "total": 0.2576,
                    "energy": 0.058,
                    "tax": 0.1996,
                    "startsAt": "2024-04-20T01:00:00.000+02:00",
                },
                {
                    "total": 0.2568,
                    "energy": 0.0573,
                    "tax": 0.1995,
                    "startsAt": "2024-04-20T02:00:00.000+02:00",
                },
                {
                    "total": 0.2573,
                    "energy": 0.0578,
                    "tax": 0.1995,
                    "startsAt": "2024-04-20T03:00:00.000+02:00",
                },
                {
                    "total": 0.2613,
                    "energy": 0.061,
                    "tax": 0.2003,
                    "startsAt": "2024-04-20T04:00:00.000+02:00",
                },
                {
                    "total": 0.2634,
                    "energy": 0.0628,
                    "tax": 0.2006,
                    "startsAt": "2024-04-20T05:00:00.000+02:00",
                },
                {
                    "total": 0.2647,
                    "energy": 0.0639,
                    "tax": 0.2008,
                    "startsAt": "2024-04-20T06:00:00.000+02:00",
                },
                {
                    "total": 0.2695,
                    "energy": 0.068,
                    "tax": 0.2015,
                    "startsAt": "2024-04-20T07:00:00.000+02:00",
                },
                {
                    "total": 0.266,
                    "energy": 0.065,
                    "tax": 0.201,
                    "startsAt": "2024-04-20T08:00:00.000+02:00",
                },
                {
                    "total": 0.2599,
                    "energy": 0.0599,
                    "tax": 0.2,
                    "startsAt": "2024-04-20T09:00:00.000+02:00",
                },
                {
                    "total": 0.2482,
                    "energy": 0.05,
                    "tax": 0.1982,
                    "startsAt": "2024-04-20T10:00:00.000+02:00",
                },
                {
                    "total": 0.2344,
                    "energy": 0.0384,
                    "tax": 0.196,
                    "startsAt": "2024-04-20T11:00:00.000+02:00",
                },
                {
                    "total": 0.2231,
                    "energy": 0.029,
                    "tax": 0.1941,
                    "startsAt": "2024-04-20T12:00:00.000+02:00",
                },
                {
                    "total": 0.2033,
                    "energy": 0.0123,
                    "tax": 0.191,
                    "startsAt": "2024-04-20T13:00:00.000+02:00",
                },
                {
                    "total": 0.2012,
                    "energy": 0.0106,
                    "tax": 0.1906,
                    "startsAt": "2024-04-20T14:00:00.000+02:00",
                },
                {
                    "total": 0.2104,
                    "energy": 0.0183,
                    "tax": 0.1921,
                    "startsAt": "2024-04-20T15:00:00.000+02:00",
                },
                {
                    "total": 0.2331,
                    "energy": 0.0374,
                    "tax": 0.1957,
                    "startsAt": "2024-04-20T16:00:00.000+02:00",
                },
                {
                    "total": 0.2634,
                    "energy": 0.0628,
                    "tax": 0.2006,
                    "startsAt": "2024-04-20T17:00:00.000+02:00",
                },
                {
                    "total": 0.2825,
                    "energy": 0.0789,
                    "tax": 0.2036,
                    "startsAt": "2024-04-20T18:00:00.000+02:00",
                },
                {
                    "total": 0.2953,
                    "energy": 0.0896,
                    "tax": 0.2057,
                    "startsAt": "2024-04-20T19:00:00.000+02:00",
                },
                {
                    "total": 0.3041,
                    "energy": 0.097,
                    "tax": 0.2071,
                    "startsAt": "2024-04-20T20:00:00.000+02:00",
                },
                {
                    "total": 0.2961,
                    "energy": 0.0903,
                    "tax": 0.2058,
                    "startsAt": "2024-04-20T21:00:00.000+02:00",
                },
                {
                    "total": 0.2911,
                    "energy": 0.0861,
                    "tax": 0.205,
                    "startsAt": "2024-04-20T22:00:00.000+02:00",
                },
                {
                    "total": 0.2873,
                    "energy": 0.0829,
                    "tax": 0.2044,
                    "startsAt": "2024-04-20T23:00:00.000+02:00",
                },
            ],
            "tomorrow": [
                {
                    "total": 0.286,
                    "energy": 0.0818,
                    "tax": 0.2042,
                    "startsAt": "2024-04-21T00:00:00.000+02:00",
                },
                {
                    "total": 0.2726,
                    "energy": 0.0706,
                    "tax": 0.202,
                    "startsAt": "2024-04-21T01:00:00.000+02:00",
                },
                {
                    "total": 0.2714,
                    "energy": 0.0695,
                    "tax": 0.2019,
                    "startsAt": "2024-04-21T02:00:00.000+02:00",
                },
                {
                    "total": 0.2653,
                    "energy": 0.0644,
                    "tax": 0.2009,
                    "startsAt": "2024-04-21T03:00:00.000+02:00",
                },
                {
                    "total": 0.2646,
                    "energy": 0.0639,
                    "tax": 0.2007,
                    "startsAt": "2024-04-21T04:00:00.000+02:00",
                },
                {
                    "total": 0.2643,
                    "energy": 0.0636,
                    "tax": 0.2007,
                    "startsAt": "2024-04-21T05:00:00.000+02:00",
                },
                {
                    "total": 0.2653,
                    "energy": 0.0644,
                    "tax": 0.2009,
                    "startsAt": "2024-04-21T06:00:00.000+02:00",
                },
                {
                    "total": 0.2607,
                    "energy": 0.0605,
                    "tax": 0.2002,
                    "startsAt": "2024-04-21T07:00:00.000+02:00",
                },
                {
                    "total": 0.2611,
                    "energy": 0.0609,
                    "tax": 0.2002,
                    "startsAt": "2024-04-21T08:00:00.000+02:00",
                },
                {
                    "total": 0.2545,
                    "energy": 0.0554,
                    "tax": 0.1991,
                    "startsAt": "2024-04-21T09:00:00.000+02:00",
                },
                {
                    "total": 0.2279,
                    "energy": 0.033,
                    "tax": 0.1949,
                    "startsAt": "2024-04-21T10:00:00.000+02:00",
                },
                {
                    "total": 0.2326,
                    "energy": 0.037,
                    "tax": 0.1956,
                    "startsAt": "2024-04-21T11:00:00.000+02:00",
                },
                {
                    "total": 0.1958,
                    "energy": 0.0061,
                    "tax": 0.1897,
                    "startsAt": "2024-04-21T12:00:00.000+02:00",
                },
                {
                    "total": 0.189,
                    "energy": 0.0003,
                    "tax": 0.1887,
                    "startsAt": "2024-04-21T13:00:00.000+02:00",
                },
                {
                    "total": 0.1876,
                    "energy": -0.0009,
                    "tax": 0.1885,
                    "startsAt": "2024-04-21T14:00:00.000+02:00",
                },
                {
                    "total": 0.1895,
                    "energy": 0.0008,
                    "tax": 0.1887,
                    "startsAt": "2024-04-21T15:00:00.000+02:00",
                },
                {
                    "total": 0.1958,
                    "energy": 0.006,
                    "tax": 0.1898,
                    "startsAt": "2024-04-21T16:00:00.000+02:00",
                },
                {
                    "total": 0.2579,
                    "energy": 0.0582,
                    "tax": 0.1997,
                    "startsAt": "2024-04-21T17:00:00.000+02:00",
                },
                {
                    "total": 0.2774,
                    "energy": 0.0746,
                    "tax": 0.2028,
                    "startsAt": "2024-04-21T18:00:00.000+02:00",
                },
                {
                    "total": 0.295,
                    "energy": 0.0894,
                    "tax": 0.2056,
                    "startsAt": "2024-04-21T19:00:00.000+02:00",
                },
                {
                    "total": 0.302,
                    "energy": 0.0953,
                    "tax": 0.2067,
                    "startsAt": "2024-04-21T20:00:00.000+02:00",
                },
                {
                    "total": 0.297,
                    "energy": 0.0911,
                    "tax": 0.2059,
                    "startsAt": "2024-04-21T21:00:00.000+02:00",
                },
                {
                    "total": 0.295,
                    "energy": 0.0894,
                    "tax": 0.2056,
                    "startsAt": "2024-04-21T22:00:00.000+02:00",
                },
                {
                    "total": 0.2939,
                    "energy": 0.0885,
                    "tax": 0.2054,
                    "startsAt": "2024-04-21T23:00:00.000+02:00",
                },
            ],
        }
        builder = SimpleDashboardBuilder()
        builder.build_dashboard({"tibber_data": test_data})
        self.fail()
