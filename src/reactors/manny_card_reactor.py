import json
import textwrap

from src.config import Config
from src.database import create_card
from src.reactors.base import EmptyReactorResult, Reactor, ReactorContext, ReactorResult
from src.utils import extract_url


class MannyCardReactor(Reactor):
    """This class has a db integration. See src/database.py"""

    emoji = "🃏"
    glif_id_data = "clumo1gze000ak7eymnp9z07j"
    glif_id_card = "clumtpbkq000011v8yedrk2en"
    collection = "mannygen"
    json_retries = 5
    text_wrapper_footer = textwrap.TextWrapper(width=65, max_lines=2, placeholder="...")
    text_wrapper_action = textwrap.TextWrapper(width=50, max_lines=2, placeholder="...")

    def __init__(self):
        super().__init__()
        self.make_single_use()
        self.retrieve_prompt_from_watchlist()
        self.add_nonce()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        inputs = {
            "prompt": context.prompt.replace("!mg ", "").replace("!mannygen ", ""),
        }
        print(f"{self.emoji} cardmaker inputs: {inputs}")

        card_data = None
        while range(self.json_retries):
            try:
                raw_card_data = await self.glif_client.arun_simple(
                    self.glif_id_data, inputs
                )
                card_data = json.loads(raw_card_data)

                # these should work
                int(card_data["hp"])
                int(card_data["move1_power"])
                int(card_data["move2_power"])

            except Exception as e:
                print(f"{self.emoji} cardmaker error: {e}, raw:{raw_card_data}")
            else:
                print(f"{self.emoji} cardmaker message content: {card_data}")
                break
        if card_data is None:
            return EmptyReactorResult()

        db_card_data = {**card_data}

        move1_info = card_data.pop("move1_info")
        lines = self.text_wrapper_action.wrap(move1_info)
        if len(lines) == 1:
            move1_info_1 = lines[0]
            move1_info_2 = ""
        else:
            move1_info_1, move1_info_2, *_ = lines

        move2_info = card_data.pop("move2_info")
        lines = self.text_wrapper_action.wrap(move2_info)
        if len(lines) == 1:
            move2_info_1 = lines[0]
            move2_info_2 = ""
        else:
            move2_info_1, move2_info_2, *_ = lines

        footer = card_data.pop("footer")
        lines = self.text_wrapper_footer.wrap(footer)
        if len(lines) == 1:
            footer_1 = lines[0]
            footer_2 = ""
        else:
            footer_1, footer_2, *_ = lines

        card_data["move1_info_1"] = move1_info_1
        card_data["move1_info_2"] = move1_info_2
        card_data["move2_info_1"] = move2_info_1
        card_data["move2_info_2"] = move2_info_2
        card_data["footer_1"] = footer_1
        card_data["footer_2"] = footer_2

        url = extract_url(context.message.content)
        if url is None:
            return EmptyReactorResult

        card_data["image_url"] = url
        card_data["nth"] = self.nonce

        card_image_url = await self.glif_client.arun_simple(
            self.glif_id_card,
            card_data,
        )

        db_card_data["image_url"] = url
        db_card_data["nth"] = self.nonce

        if not Config.DEV:
            await create_card(**db_card_data)

        return ReactorResult(content=card_image_url)
