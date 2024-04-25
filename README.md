# Overcier

Overcier is a small discord bot that enables interaction with glifs.
This is a reference implementation for the mannygen bot.

src:
- `reactors/` subdir for emoji reactors
- `app_explorer.py`: fastapi app to explore generated cards
- `app.py`: discord app
- `config.py`: config class
- `database.py`: postgresql integration
- `filters.py`: filters for messages

# Quickstart

`$ cp .env.sample .env` and fill in `.env`.

`$ poetry install && poetry shell`

`$ python src/app.py`

Run the card explorer demo with

`$ uvicorn src.app_explorer.:app`

# Example reactor

```python
from glif_client import GlifClient

from src.reactors.base import EmptyReactorResult, Reactor, ReactorContext, ReactorResult
from src.utils import extract_url


class BackgroundRemoverReactor(Reactor):
    # always set these attributes
    emoji = "✂️"
    glif_id = "clul69qgs0002e6gragrswsl4"

    def __init__(self):
        super().__init__()
        # the functions below add hooks for behavior
        # uncomment the hooks to enable them
        # these functions are defined in src/reactors/base.py

        # makes the reactor single use
        self.make_single_use()
        
        # gets the prompt from the global watchlist and puts it in the context
        # self.retrieve_prompt_from_watchlist()
        
        # adds the result to the global watchlist
        # self.add_result_to_watchlist()
        
        # adds a nonce attribute to keep track of generations
        # self.add_nonce()

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
```