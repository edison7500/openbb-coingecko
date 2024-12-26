"""CoinGecko Provider Module."""

from openbb_coingecko_provider.models.coingecko import CoingeckoOHLCFetcher
from openbb_core.provider.abstract.provider import Provider

coingecko_provider = Provider(
    name="coingecko", # This should be the same as the assigned name at the bottom of the pyproject.toml file
    website="https://www.coingecko.com/",
    description="""coingecko provider is a supplier of crypto.""",
    #credentials=["api_key"], # uncomment to require credentials
    fetcher_dict={
         "CoingeckoOHLC": CoingeckoOHLCFetcher,
    },
)
