from src.reactors.base import EmptyReactorResult, Reactor, ReactorContext, ReactorResult
from src.utils import extract_url


class BackgroundRemoverReactor(Reactor):
    emoji = "✂️"
    glif_id = "clul69qgs0002e6gragrswsl4"
    collection = "mannygen"

    def __init__(self):
        super().__init__()
        self.make_single_use()

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
