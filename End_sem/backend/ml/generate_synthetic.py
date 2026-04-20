"""
Generate synthetic EV charging station data when real CSV data is unavailable.

This enables the model to auto-train on Render or any fresh deployment
where the large CSV files are not present (they are gitignored).

The synthetic data mimics realistic patterns:
  - Hourly demand with morning/evening peaks
  - Day-of-week seasonality (weekdays vs weekends)
  - Correlated features (price ↔ demand, solar ↔ time-of-day)
  - Noise for realistic variance
"""

from __future__ import annotations

import os
import math
import random
from datetime import datetime, timedelta
from typing import List, Dict

import numpy as np
import pandas as pd


def _generate_hourly_demand(hour: int, day_of_week: int, noise_scale: float = 0.08) -> float:
    """Realistic EV charging demand curve with double-peak pattern."""
    # Morning peak at 8 AM, evening peak at 6-8 PM
    morning_peak = 0.7 * math.exp(-0.5 * ((hour - 8) / 2.5) ** 2)
    evening_peak = 1.0 * math.exp(-0.5 * ((hour - 19) / 3.0) ** 2)
    # Midday baseline
    baseline = 0.15 + 0.05 * math.sin(math.pi * hour / 24)
    # Weekend adjustment (lower demand)
    weekend_factor = 0.75 if day_of_week >= 5 else 1.0
    # Combine
    demand = (baseline + morning_peak + evening_peak) * weekend_factor
    # Add noise
    demand += random.gauss(0, noise_scale)
    return max(0.01, demand)


def _generate_price(hour: int, demand: float) -> float:
    """Electricity price correlated with demand and time-of-use."""
    base_price = 0.10
    peak_surcharge = 0.08 * math.exp(-0.5 * ((hour - 18) / 4) ** 2)
    demand_factor = 0.02 * demand
    noise = random.gauss(0, 0.005)
    return max(0.05, base_price + peak_surcharge + demand_factor + noise)


def _generate_solar(hour: int) -> float:
    """Solar production follows daylight curve."""
    if hour < 6 or hour > 20:
        return 0.0
    peak = 45.0  # kW peak
    return max(0, peak * math.sin(math.pi * (hour - 6) / 14) + random.gauss(0, 3))


def _generate_wind() -> float:
    """Wind production with random variability."""
    return max(0, random.gauss(15, 8))


def generate_synthetic_csv(
    output_dir: str,
    filename: str = "synthetic_station_data.csv",
    n_days: int = 90,
    seed: int = 42,
) -> str:
    """
    Generate a synthetic CSV file that matches the schema of real station data.

    Returns the path to the generated CSV file.
    """
    random.seed(seed)
    np.random.seed(seed)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    start_date = datetime(2025, 1, 1)
    rows: List[Dict] = []

    for day_offset in range(n_days):
        current_date = start_date + timedelta(days=day_offset)
        day_of_week = current_date.weekday()

        for hour in range(24):
            dt = current_date + timedelta(hours=hour)

            demand = _generate_hourly_demand(hour, day_of_week)
            price = _generate_price(hour, demand)
            solar = _generate_solar(hour)
            wind = _generate_wind()
            n_evs = max(1, int(demand * 8 + random.gauss(0, 2)))
            grid_stability = max(0.5, min(1.5, 1.0 + random.gauss(0, 0.1) - 0.1 * (demand > 0.8)))
            station_capacity = 150.0  # kW fixed
            peak_demand = demand * (1.1 + random.uniform(0, 0.2))
            renewable_pct = min(100, max(0, (solar + wind) / station_capacity * 100 + random.gauss(0, 5)))
            efficiency = min(100, max(70, 92 + random.gauss(0, 3)))
            battery_storage = max(0, 50 + random.gauss(0, 10))
            total_renewable = solar + wind

            rows.append({
                "Date": dt.strftime("%Y-%m-%d"),
                "Time": dt.strftime("%H:%M:%S"),
                "EV Charging Demand (kW)": round(demand, 6),
                "Electricity Price ($/kWh)": round(price, 4),
                "Grid Stability Index": round(grid_stability, 4),
                "Number of EVs Charging": n_evs,
                "Solar Energy Production (kW)": round(solar, 2),
                "Wind Energy Production (kW)": round(wind, 2),
                "Charging Station Capacity (kW)": station_capacity,
                "Peak Demand (kW)": round(peak_demand, 4),
                "Renewable Energy Usage (%)": round(renewable_pct, 2),
                "EV Charging Efficiency (%)": round(efficiency, 2),
                "Battery Storage (kWh)": round(battery_storage, 2),
                "Total Renewable Energy Production (kW)": round(total_renewable, 2),
            })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"[synthetic] Generated {len(df)} rows → {output_path}")
    return output_path


if __name__ == "__main__":
    # Generate into the data/ directory relative to backend/
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(backend_dir, "data")
    generate_synthetic_csv(data_dir)
