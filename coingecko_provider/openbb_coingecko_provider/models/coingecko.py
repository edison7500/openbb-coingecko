"""Coingecko Provider Models."""
import httpx
import pandas as pd
from dateutil import parser
from datetime import (
    date as dateType,
    datetime
)
from typing import Any, Dict, List, Optional, Union

from openbb_core.provider.utils.descriptions import (
    DATA_DESCRIPTIONS,
    QUERY_DESCRIPTIONS,
)
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from openbb_core.provider.abstract.data import Data
from pydantic import Field, PositiveInt, PositiveFloat, field_validator


class CoingeckoHistoricalQueryParams(QueryParams):
    symbol: str = Field(
        description=QUERY_DESCRIPTIONS.get("symbol", "")
        + " Can use coin id format."
    )
    vs_currency: str = Field()
    days: PositiveInt = Field()


class CoingeckoHistoricalData(Data):
    """Crypto Historical Price Data."""

    date: Union[dateType, datetime] = Field(
        description=DATA_DESCRIPTIONS.get("date", "")
    )
    open: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("open", ""))
    high: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("high", ""))
    low: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("low", ""))
    close: PositiveFloat = Field(description=DATA_DESCRIPTIONS.get("close", ""))

    @field_validator("date", mode="before", check_fields=False)
    @classmethod
    def date_validate(cls, v):  # pylint: disable=E0213
        """Return formatted datetime."""
        if ":" in str(v):
            return parser.isoparse(str(v))
        return parser.parse(str(v)).date()


class CoingeckoOHLCFetcher(
    Fetcher[
        CoingeckoHistoricalQueryParams,
        List[CoingeckoHistoricalData],
    ]
):
    @staticmethod
    def transform_query(params: Dict[str, Any]) -> CoingeckoHistoricalQueryParams:
        """Transform query params."""
        return CoingeckoHistoricalQueryParams(**params)

    @staticmethod
    async def aextract_data( # The function does not have to be asynchronous. If not, remove the leading 'a', 'extract_data'.
        query: CoingeckoHistoricalQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Extract data. Put HTTP Requests here. This should return the closest form of raw data possible."""
        print(query)
        url = f"https://api.coingecko.com/api/v3/coins/{query.symbol}/ohlc?vs_currency={query.vs_currency}&days={query.days}"
        client = httpx.AsyncClient()
        res = await client.get(url)
        # data = response.json()
        df = pd.DataFrame(res.json(), columns=["date", "open", "high", "low", "close"])
        df.date = df.date.apply(lambda x : datetime.fromtimestamp(x / 1000))

        return df.to_dict(orient="records")

    @staticmethod
    def transform_data(
        query: CoingeckoHistoricalQueryParams,
        data: List[Dict],
        **kwargs: Any
    ) -> List[CoingeckoHistoricalData]:
        return [CoingeckoHistoricalData.model_validate(d) for d in data]
