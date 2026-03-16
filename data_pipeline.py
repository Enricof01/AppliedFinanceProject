import requests
import pandas as pd

def load_bitget_btcusdt_5m(limit: int = 320) -> pd.DataFrame:
    url = "https://api.bitget.com/api/v2/mix/market/candles"
    params = {
        "symbol": "BTCUSDT",
        "productType": "USDT-FUTURES",
        "granularity": "15m",
        "limit": str(limit),
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    payload = r.json()

    if payload.get("code") != "00000":
        raise RuntimeError(f"Bitget API error: {payload}")

    rows = payload.get("data", [])
    if not rows:
        raise RuntimeError("No candle data returned")

    # Bitget returns arrays like:
    # [timestamp, open, high, low, close, baseVolume, quoteVolume]
    df = pd.DataFrame(rows)
    if df.shape[1] < 5:
        raise RuntimeError(f"Unexpected candle format: {rows[:3]}")

    df = df.iloc[:, :7]
    df.columns = ["timestamp", "open", "high", "low", "close", "base_volume", "quote_volume"]

    df["timestamp"] = pd.to_datetime(df["timestamp"].astype("int64"), unit="ms", utc=True)
    for col in ["open", "high", "low", "close", "base_volume", "quote_volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

df = load_bitget_btcusdt_5m()
# print(df.head())
# print(df.tail())