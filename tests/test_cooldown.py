"""Cooldown gate uses exchange timestamp (VWAP strategy)."""

from __future__ import annotations

import datetime
import unittest

from trading_engine.calendar.taifex import TAIWAN_TZ
from trading_engine.testing.defaults import default_test_settings

from tests.helpers import make_vwap_host


class TestCooldownUsesExchangeTs(unittest.TestCase):
    def test_cooldown_blocks_until_exchange_ts_elapsed(self):
        s = default_test_settings()
        host = make_vwap_host()
        exit_ts = 1_700_000_000
        host.last_exit_time = exit_ts
        host.current_atr = 100.0

        during = host.process_strategy(
            exit_ts + s.cooldown_sec - 1,
            18000.0,
            datetime.datetime.fromtimestamp(
                exit_ts + s.cooldown_sec - 1, tz=TAIWAN_TZ
            ),
        )
        self.assertIsNone(during)


if __name__ == "__main__":
    unittest.main()
