from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_transformer_data(
    num_feeders: int = 40,
    output_path: str | Path = "data/transformer_data.csv",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate synthetic but realistic distribution transformer loading data.
    """
    if not 30 <= num_feeders <= 50:
        raise ValueError("num_feeders must be between 30 and 50.")

    rng = np.random.default_rng(seed)

    capacities = rng.integers(200, 1001, size=num_feeders)
    load_ratio = rng.uniform(0.60, 0.98, size=num_feeders)
    current_load = np.round(capacities * load_ratio, 2)
    temperature = np.round(rng.uniform(30, 50, size=num_feeders), 1)
    growth = np.round(rng.uniform(1, 10, size=num_feeders), 2)

    df = pd.DataFrame(
        {
            "Feeder_ID": [f"F-{i:02d}" for i in range(1, num_feeders + 1)],
            "Transformer_Capacity_kVA": capacities,
            "Current_Load_kVA": current_load,
            "Temperature_C": temperature,
            "Historical_Growth_Percent": growth,
        }
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    generate_transformer_data()
