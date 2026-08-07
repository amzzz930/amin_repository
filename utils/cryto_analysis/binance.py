import requests
import pandas as pd


class BinanceAnalyst:
    """
    This gets data with high frequency (i.e 5 minutely) but not for many days
    """

    def __init__(
        self,
        coin: str = "ETH",
        currency: str = "USDT",
    ):
        self.coin_symbol = f"{coin}{currency}".upper()
        self.endpoint = "https://api.binance.com"

    def get_coin_data(self, interval: str = "5m", limit: int = 500) -> str | int:
        """iterates through coins/list"""
        url = f"{self.endpoint}/api/v3/klines"
        params = {"symbol": self.coin_symbol, "interval": interval, "limit": limit}
        r = requests.get(url, params=params)
        data = r.json()

        df = pd.DataFrame(
            data,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )

        df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
