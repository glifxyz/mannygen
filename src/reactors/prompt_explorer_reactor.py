import json

from src.reactors.base import Reactor, ReactorContext, ReactorResult


class PromptExplorerUpReactor(Reactor):
    emoji = "⬆️"
    glif_id = "clv3pw40z00002rrjxlurnzjr"
    collection = "prompt_explorer"

    def __init__(self):
        super().__init__()
        self.retrieve_prompt_from_watchlist()
        self.add_result_to_watchlist()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        output = await self.glif_client.arun_simple(
            self.glif_id,
            {"direction": "up", "location": context.prompt},
        )
        output = json.loads(output)

        return ReactorResult(content=output["image_url"], prompt=output["location"])


class PromptExplorerRightReactor(Reactor):
    emoji = "➡️"
    glif_id = "clv3pw40z00002rrjxlurnzjr"
    collection = "prompt_explorer"

    def __init__(self):
        super().__init__()
        self.retrieve_prompt_from_watchlist()
        self.add_result_to_watchlist()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        output = await self.glif_client.arun_simple(
            self.glif_id,
            {"direction": "up", "location": context.prompt},
        )
        output = json.loads(output)

        return ReactorResult(content=output["image_url"], prompt=output["location"])


class PromptExplorerDownReactor(Reactor):
    emoji = "⬇️"
    glif_id = "clv3pw40z00002rrjxlurnzjr"
    collection = "prompt_explorer"

    def __init__(self):
        super().__init__()
        self.retrieve_prompt_from_watchlist()
        self.add_result_to_watchlist()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        output = await self.glif_client.arun_simple(
            self.glif_id,
            {"direction": "up", "location": context.prompt},
        )
        output = json.loads(output)

        return ReactorResult(content=output["image_url"], prompt=output["location"])


class PromptExplorerLeftReactor(Reactor):
    emoji = "⬅"
    glif_id = "clv3pw40z00002rrjxlurnzjr"
    collection = "prompt_explorer"

    def __init__(self):
        super().__init__()
        self.retrieve_prompt_from_watchlist()
        self.add_result_to_watchlist()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        output = await self.glif_client.arun_simple(
            self.glif_id,
            {"direction": "up", "location": context.prompt},
        )
        output = json.loads(output)

        return ReactorResult(content=output["image_url"], prompt=output["location"])
