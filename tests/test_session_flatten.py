"""Session flatten behavior via VWAP momentum strategy."""

from __future__ import annotations

import datetime
import unittest

from trading_engine.testing.defaults import default_test_settings

from tests.helpers import make_vwap_host


def _dt(hour: int, minute: int, second: int = 0) -> datetime.datetime:
    return datetime.datetime(2026, 6, 10, hour, minute, second)


class TestSessionFlattenStrategy(unittest.TestCase):
    def setUp(self) -> None:
        self.s = default_test_settings()

    def test_force_flatten_signal(self):
        host = make_vwap_host()
        host.has_position = True
        host.position_dir = "Long"
        host.entry_price = 18000.0
        ts = int(_dt(13, 44).timestamp())

        signal = host.process_strategy(ts, 17990.0, _dt(13, 44))

        self.assertIsNotNone(signal)
        assert signal is not None
        self.assertEqual(signal.action, "Sell")
        self.assertEqual(signal.intent, "exit")
        self.assertEqual(signal.slippage_points, self.s.flatten_slippage_points)
        self.assertIsNotNone(signal.audit)
        assert signal.audit is not None
        self.assertEqual(signal.audit.reason, "session_force_flatten")

    def test_no_entry_after_flatten_time(self):
        host = make_vwap_host()
        host.current_atr = 100.0
        ts = int(_dt(13, 40).timestamp())

        signal = host.process_strategy(ts, 18000.0, _dt(13, 40))

        self.assertIsNone(signal)

    def test_force_flatten_overrides_manage_exit(self):
        host = make_vwap_host()
        host.has_position = True
        host.position_dir = "Long"
        host.entry_price = 18000.0
        host.trailing_peak = 18000.0
        ts = int(_dt(13, 44).timestamp())

        signal = host.process_strategy(ts, 18000.0, _dt(13, 44))

        self.assertIsNotNone(signal)
        assert signal is not None
        self.assertEqual(signal.audit.reason, "session_force_flatten")


if __name__ == "__main__":
    unittest.main()
