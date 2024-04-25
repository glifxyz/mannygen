from collections import deque
from collections.abc import MutableSequence
from dataclasses import dataclass
from typing import Optional

from discord import Message, User
from glif_client import GlifClient


@dataclass
class ReactorContext:
    message: Message
    user: User
    halt: bool = False
    prompt: Optional[str] = None
    reaction_watchlist: Optional[MutableSequence] = None


@dataclass
class WatchlistTuple:
    id: str
    prompt: str
    collection: Optional[str] = None


@dataclass
class ReactorResult:
    content: str
    prompt: Optional[str] = None
    add_to_watchlist: bool = False


class EmptyReactorResult(ReactorResult):
    content: str = ""


class Reactor:
    emoji: str
    glif_id: str
    collection: str

    def __init__(self):
        self._run_before = []
        self._run_after = []

    async def _run(self, context: ReactorContext) -> ReactorResult:
        raise NotImplementedError

    async def run(self, context: ReactorContext) -> ReactorResult:
        for func in self._run_before:
            print(f"_run_before: {func}")
            context = func(context)
            if context.halt:
                return EmptyReactorResult()

        result = await self._run(context)

        for func in self._run_after:
            print(f"_run_after: {func}")
            result = func(context, result)

        return result

    def set_glif_client(self, glif_client: GlifClient) -> "Reactor":
        self.glif_client = glif_client
        return self

    def make_single_use(self) -> "Reactor":
        self.single_use_list = deque(maxlen=1000)

        def check_before(context: ReactorContext) -> ReactorContext:
            if context.message.id in self.single_use_list:
                print("single use check ")
                context.halt = True
            return context

        self._run_before.append(check_before)

        def add_to_single_use_list(
            context: ReactorContext, result: ReactorResult
        ) -> ReactorResult:
            self.single_use_list.append(context.message.id)
            return result

        self._run_after.append(add_to_single_use_list)
        return self

    def retrieve_prompt_from_watchlist(self) -> "Reactor":
        def retrieve_prompt(context):
            for watchlist_tuple in context.reaction_watchlist:
                if watchlist_tuple.id == context.message.id:
                    context.prompt = watchlist_tuple.prompt
                    break
            return context

        self._run_before.append(retrieve_prompt)
        return self

    def add_result_to_watchlist(self) -> "Reactor":
        def add_to_watchlist(
            context: ReactorContext, result: ReactorResult
        ) -> ReactorResult:
            result.add_to_watchlist = True
            if result.prompt is None:
                result.prompt = context.prompt
            return result

        self._run_after.append(add_to_watchlist)
        return self

    def add_nonce(self):
        self.nonce = 1

        def increment_nonce(
            context: ReactorContext, result: ReactorResult
        ) -> ReactorResult:
            self.nonce += 1
            return result

        self._run_after.append(increment_nonce)
        return self
