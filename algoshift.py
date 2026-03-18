"""
Algoshift: computational implementation for labor economics analysis.

Algoshift refers to labor scheduling where algorithms dynamically adjust worker hours based on real-time demand predictions, creating unpredictability and externalizing scheduling costs onto workers. This module provides a reproducible calculator that validates the canonical channels, normalizes each series, computes a weighted index, and supports simple counterfactual policy simulation. The design is intentionally transparent so researchers can inspect how the concept moves from definition to code. Typical uses include comparative diagnostics, notebook-based scenario testing, and integration into empirical pipelines where consistent measurement matters as much as prediction.
"""
from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

# Algoshift channels track the observable anatomy of the canonical definition.
TERM_CHANNELS = [
    "demand_uncertainty",  # Demand uncertainty captures a distinct economic channel.
    "algorithmic_control",  # Algorithmic control captures a distinct economic channel.
    "shift_variability",  # Shift variability captures a distinct economic channel.
    "worker_autonomy",  # Worker autonomy mitigates exposure when it is high.
    "schedule_notice_hours",  # Schedule notice hours mitigates exposure when it is high.
    "income_volatility",  # Income volatility captures a distinct economic channel.
    "turnover_risk",  # Turnover risk captures a distinct economic channel.
]

# Weighted channels preserve the repository's existing score logic.
WEIGHTED_CHANNELS = [
    "demand_uncertainty",
    "algorithmic_control",
    "shift_variability",
    "worker_autonomy",
    "schedule_notice_hours",
    "income_volatility",
    "turnover_risk",
]

# Default weights encode the relative economic importance of each weighted channel.
DEFAULT_WEIGHTS: dict[str, float] = {
    "demand_uncertainty": 0.17,  # Demand uncertainty captures a distinct economic channel.
    "algorithmic_control": 0.19,  # Algorithmic control captures a distinct economic channel.
    "shift_variability": 0.21,  # Shift variability captures a distinct economic channel.
    "worker_autonomy": 0.12,  # Worker autonomy mitigates exposure when it is high.
    "schedule_notice_hours": 0.11,  # Schedule notice hours mitigates exposure when it is high.
    "income_volatility": 0.12,  # Income volatility captures a distinct economic channel.
    "turnover_risk": 0.08,  # Turnover risk captures a distinct economic channel.
}


class AlgoshiftCalculator:
    """
    Compute Algoshift index scores from tabular data.

    Parameters
    ----------
    weights : dict[str, float] | None
        Optional weights overriding DEFAULT_WEIGHTS. Keys must match
        WEIGHTED_CHANNELS and values must sum to 1.0.
    """

    def __init__(self, weights: Optional[dict[str, float]] = None) -> None:
        # Alternative weights are useful for robustness checks across specifications.
        self.weights = weights or DEFAULT_WEIGHTS.copy()

        # Exact key matching prevents silent omission of economically relevant channels.
        if set(self.weights) != set(WEIGHTED_CHANNELS):
            raise ValueError(f"Weights must include exactly these channels: {WEIGHTED_CHANNELS}")

        # Unit-sum weights keep the index interpretable across datasets.
        if abs(sum(self.weights.values()) - 1.0) >= 1e-6:
            raise ValueError("Weights must sum to 1.0")

    @staticmethod
    def _normalise(series: pd.Series) -> pd.Series:
        """
        Return min-max normalized values on the unit interval.
        """
        lo = float(series.min())
        hi = float(series.max())
        if hi == lo:
            # Degenerate channels should not create spurious variation.
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - lo) / (hi - lo)

    def calculate_algoshift(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute normalized channels, composite scores, and qualitative bands.
        """
        # Full channel validation keeps the score tied to the canonical definition.
        missing = [channel for channel in TERM_CHANNELS if channel not in df.columns]
        if missing:
            raise ValueError(f"Missing Algoshift channels: {missing}")

        out = df.copy()
        for channel in TERM_CHANNELS:
            out[f"{channel}_norm"] = self._normalise(out[channel])

        # Positive channels intensify the mechanism while negative channels offset it.
        out["algoshift_index"] = (
            + self.weights["demand_uncertainty"] * out["demand_uncertainty_norm"]
            + self.weights["algorithmic_control"] * out["algorithmic_control_norm"]
            + self.weights["shift_variability"] * out["shift_variability_norm"]
            + self.weights["income_volatility"] * out["income_volatility_norm"]
            + self.weights["turnover_risk"] * out["turnover_risk_norm"]
            + self.weights["worker_autonomy"] * (1.0 - out["worker_autonomy_norm"])
            + self.weights["schedule_notice_hours"] * (1.0 - out["schedule_notice_hours_norm"])
        )

        # Three bands keep the metric usable in audits, papers, and dashboards.
        out["algoshift_band"] = pd.cut(
            out["algoshift_index"],
            bins=[-np.inf, 0.33, 0.66, np.inf],
            labels=["low", "moderate", "high"],
        )
        return out

    def simulate_policy(self, df: pd.DataFrame, channel: str, reduction: float = 0.2) -> pd.DataFrame:
        """
        Simulate a policy shock that reduces one observed channel.
        """
        if channel not in TERM_CHANNELS:
            raise ValueError(f"Unknown Algoshift channel: {channel}")
        if reduction < 0.0 or reduction > 1.0:
            raise ValueError("reduction must be between 0.0 and 1.0")

        # Counterfactual shocks translate reforms into score movements.
        df_policy = df.copy()
        df_policy[channel] = df_policy[channel] * (1 - reduction)
        return self.calculate_algoshift(df_policy)


if __name__ == "__main__":
    sample = pd.read_csv("algoshift_dataset.csv")
    calc = AlgoshiftCalculator()
    print(calc.calculate_algoshift(sample)[["algoshift_index", "algoshift_band"]].head(10).to_string(index=False))

    scenario = calc.simulate_policy(sample, channel="demand_uncertainty", reduction=0.15)
    print("\nPolicy Scenario Mean Index:")
    print(float(scenario["algoshift_index"].mean()))
