
import os
import pandas as pd
import requests
from pathlib import Path

DEFAULT_DATA_PATH = Path("/opt/axentx/surrogate-1/data/usage.csv")
ENV_DATA_PATH_VAR = "USAGE_DATA_PATH"

def _resolve_data_path() -> Path:
    """Resolve the CSV file path, honoring the environment variable."""
    env_path = os.getenv(ENV_DATA_PATH_VAR)
    if env_path:
        return Path(env_path).expanduser().resolve()
    return DEFAULT_DATA_PATH

def load_usage_data_from_csv(csv_path: Optional[Path] = None) -> pd.Series:
    """
    Load raw usage data from a CSV file and return a time-indexed Series.
    """
    path = csv_path or _resolve_data_path()
    if not path.is_file():
        raise FileNotFoundError(f"Usage data file not found: {path}")

    df = pd.read_csv(path, parse_dates=["timestamp"])
    if "usage" not in df.columns:
        raise ValueError("CSV must contain a 'usage' column")

    df["timestamp"] = df["timestamp"].dt.tz_convert("UTC")
    df = df.set_index("timestamp").sort_index()
    series = df["usage"].astype(float).resample("H").ffill()
    return series

def get_usage_data_from_api():
    """Fetch usage data from the API."""
    response = requests.get('https://api.axentx.com/v1/usage-data')
    data = response.json()
    return pd.DataFrame(data)

def get_recent_usage(hours: int = 24 * 7 * 4) -> pd.Series:
    """
    Retrieve the most recent *hours* of usage data.
    """
    try:
        # Try loading from CSV first
        full_series = load_usage_data_from_csv()
    except FileNotFoundError:
        # Fallback to API if CSV is not available
        data = get_usage_data_from_api()
        full_series = pd.Series(data['usage'], index=pd.to_datetime(data['timestamp']))

    if len(full_series) == 0:
        raise RuntimeError("No usage data available for forecasting")
    return full_series.last(f"{hours}H")