"""Coingecko Router"""

# from typing import Any, Dict, List, Literal, Optional
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.provider_interface import (
    ExtraParams,
    ProviderChoices,
    StandardParams,
)
from openbb_core.provider.abstract.data import Data
from openbb_core.app.query import Query
from openbb_core.app.router import Router


router = Router(
    prefix="/price", description="Coingecko OpenBB Router Extension."
)


# This is a clone of `obb.crypto.price.historical`.
# The model can be replaced with a a different model from the Provider Interface.
@router.command(
    model="CoingeckoOHLC",
)
async def historical(
    cc: CommandContext,
    provider_choices: ProviderChoices,
    standard_params: StandardParams,
    extra_params: ExtraParams,
) -> OBBject[Data]:
    """An empty function using the Provider Interface."""
    return await OBBject.from_query(Query(**locals()))
