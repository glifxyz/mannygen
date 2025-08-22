import json
import textwrap

from src.config import Config
from src.database import create_card
from src.reactors.base import EmptyReactorResult, Reactor, ReactorContext, ReactorResult
from src.utils import extract_url


class MannyGunReactor(Reactor):
    """This class has a db integration. See src/database.py"""

    emoji = "🔫"
    glif_id = "cmemgni6j0000js04tgky4qcb"
    collection = "mannygen"

    def __init__(self):
        super().__init__()
        self.make_single_use()
        self.retrieve_prompt_from_watchlist()
        self.add_nonce()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        image_url = extract_url(context.message.content)
        if image_url is None:
            return EmptyReactorResult()

        image_url = await self.glif_client.arun_simple(
            self.glif_id,
            {
                "image_url": image_url,
            },
        )

        return ReactorResult(
            content=image_url,
        )
