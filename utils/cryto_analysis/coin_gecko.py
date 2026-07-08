import requests
import pandas as pd


class CGAnalyst:
    """gets data for last 7 days, per hour"""

    def __init__(
        self,
        coin: str = "ethereum",
    ):
        self.coin = coin
        self.endpoint = f"https://api.coingecko.com/api/v3"
        self.coin_id = self.get_coin_id()

    def get_coin_id(self) -> str | int:
        """iterates through coins/list"""
        url = f"{self.endpoint}/coins/list"
        r = requests.get(url)
        data = r.json()

        match = next(x for x in data if x["name"].lower() == self.coin.lower())
        id = match["id"]

        return id

    def get_coin_data(
        self, days: int = 7, vs_currency: str = "gbp", interval: str = "hourly"
    ) -> pd.DataFrame:
        url = f"{self.endpoint}/coins/{self.coin_id}/market_chart"
        params = {"days": days, "vs_currency": vs_currency, "interval": interval}
        r = requests.get(url, params=params)
        data = r.json()

        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df["timestamp_floor"] = df["timestamp"].dt.floor("h")

        return df
