from src.reactors.base import EmptyReactorResult, Reactor, ReactorContext, ReactorResult
from src.utils import extract_url, prep_manny_prompt


class AvatarRemixReactor(Reactor):
    emoji = "🔀"
    glif_id = "clus5tx9b0005y4tx1meveyzs"
    collection = "mannygen"

    def __init__(self):
        super().__init__()
        self.retrieve_prompt_from_watchlist()
        self.add_result_to_watchlist()

    async def _run(self, context: ReactorContext) -> ReactorResult:
        prompt = prep_manny_prompt(context.prompt)
        avatar_url = context.user.display_avatar

        # get the url from the content
        base_image_url = extract_url(str(context.message.content))
        if base_image_url is None:
            return EmptyReactorResult()

        image_url = await self.glif_client.arun_simple(
            self.glif_id,
            {
                "base_image": base_image_url,
                "style_image": str(avatar_url),
                "prompt": prompt,
            },
        )

        return ReactorResult(
            content=f"remixed with <@{context.user.id}>'s avatar: {image_url}",
        )
