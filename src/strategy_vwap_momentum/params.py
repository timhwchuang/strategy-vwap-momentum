"""Strategy parameter bundle — reads from injected RuntimeConfig overlay."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

from trading_engine.core.runtime_config import RuntimeConfig, SWEEP_FIELD_TO_CONST

SWEEPABLE_PARAMS = frozenset(SWEEP_FIELD_TO_CONST.values())


@dataclass
class StrategyParams:
    """Runtime strategy constants bound to a RuntimeConfig instance."""

    _cfg: RuntimeConfig

    def _live(self, const: str, snake: str) -> Any:
        return self._cfg.live_get(const, getattr(self._cfg, snake))

    @property
    def entry_band_points(self) -> float:
        return float(self._live("ENTRY_BAND_POINTS", "entry_band_points"))

    @property
    def vwap_stop_points(self) -> float:
        return float(self._live("VWAP_STOP_POINTS", "vwap_stop_points"))

    @property
    def exhaustion_vol(self) -> int:
        return int(self._live("EXHAUSTION_VOL", "exhaustion_vol"))

    @property
    def exit_grace_ticks(self) -> int:
        return int(self._live("EXIT_GRACE_TICKS", "exit_grace_ticks"))

    @property
    def exit_grace_sec(self) -> int:
        return int(self._live("EXIT_GRACE_SEC", "exit_grace_sec"))

    @property
    def fixed_tp_points(self) -> float:
        return float(self._live("FIXED_TP_POINTS", "fixed_tp_points"))

    @property
    def trail_points(self) -> float:
        return float(self._live("TRAIL_POINTS", "trail_points"))

    @property
    def hard_stop_points(self) -> float:
        return float(self._live("HARD_STOP_POINTS", "hard_stop_points"))

    @property
    def momentum_buy_ratio(self) -> float:
        return float(self._live("MOMENTUM_BUY_RATIO", "momentum_buy_ratio"))

    @property
    def momentum_sell_ratio(self) -> float:
        return float(self._live("MOMENTUM_SELL_RATIO", "momentum_sell_ratio"))

    @property
    def min_atr_threshold(self) -> float:
        return float(self._live("MIN_ATR_THRESHOLD", "min_atr_threshold"))

    @property
    def max_consecutive_loss(self) -> int:
        return int(self._live("MAX_CONSECUTIVE_LOSS", "max_consecutive_loss"))

    @property
    def atr_trailing_enabled(self) -> bool:
        return bool(self._live("ATR_TRAILING_ENABLED", "atr_trailing_enabled"))

    @property
    def atr_vwap_stop_enabled(self) -> bool:
        return bool(self._live("ATR_VWAP_STOP_ENABLED", "atr_vwap_stop_enabled"))

    @property
    def trail_points_floor(self) -> float:
        return float(self._live("TRAIL_POINTS_FLOOR", "trail_points_floor"))

    @property
    def trail_atr_k(self) -> float:
        return float(self._live("TRAIL_ATR_K", "trail_atr_k"))

    @property
    def vwap_stop_points_floor(self) -> float:
        return float(self._live("VWAP_STOP_POINTS_FLOOR", "vwap_stop_points_floor"))

    @property
    def vwap_stop_atr_k(self) -> float:
        return float(self._live("VWAP_STOP_ATR_K", "vwap_stop_atr_k"))

    @property
    def trend_filter_enabled(self) -> bool:
        return bool(self._live("TREND_FILTER_ENABLED", "trend_filter_enabled"))

    @property
    def flatten_slippage_points(self) -> int:
        return int(self._live("FLATTEN_SLIPPAGE_POINTS", "flatten_slippage_points"))

    @classmethod
    def from_runtime_config(cls, cfg: RuntimeConfig) -> StrategyParams:
        return cls(_cfg=cfg)


def sweepable_value(name: str, cfg: RuntimeConfig | None = None) -> Any:
    if cfg is None:
        raise ValueError("cfg is required")
    return cfg.live_get(name, getattr(cfg, name.lower(), None))


def apply_strategy_params(
    params: dict[str, Any], cfg: RuntimeConfig
) -> dict[str, Any]:
    return cfg.apply_overlay(params)


def restore_strategy_params(saved: dict[str, Any], cfg: RuntimeConfig) -> None:
    cfg.restore_overlay(saved)


@contextmanager
def patch_strategy_params(
    params: dict[str, Any], cfg: RuntimeConfig
) -> Iterator[RuntimeConfig]:
    saved = cfg.apply_overlay(params)
    try:
        yield cfg
    finally:
        cfg.restore_overlay(saved)


__all__ = [
    "SWEEPABLE_PARAMS",
    "SWEEP_FIELD_TO_CONST",
    "StrategyParams",
    "apply_strategy_params",
    "patch_strategy_params",
    "restore_strategy_params",
    "sweepable_value",
]