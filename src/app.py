# bot.py
import json
from collections import deque
from typing import Optional

import discord
from discord import Message
from glif_client import GlifClient
from reactors.avatar_remix_reactor import AvatarRemixReactor
from reactors.background_remover_reactor import BackgroundRemoverReactor
from reactors.base import ReactorContext, WatchlistTuple
from reactors.manny_card_reactor import MannyCardReactor
from reactors.prompt_explorer_reactor import (
    PromptExplorerDownReactor,
    PromptExplorerLeftReactor,
    PromptExplorerRightReactor,
    PromptExplorerUpReactor,
)
from rich import print

from src.config import Config
from src.database import get_len
from src.filters import check_manny_command, check_promptexplorer_command
from src.utils import NSFWError, prep_manny_prompt

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
glif_client = GlifClient()


#
# Generators
#


async def generate_manny_image(prompt: str) -> str:
    prepped_prompt = prep_manny_prompt(prompt)

    image_url = await glif_client.arun_simple(
        "clus5l9sp0000b22hzpkz5rwj",
        {
            "prompt": prepped_prompt,
        },
    )

    if image_url in [
        "https://res.cloudinary.com/dzkwltgyd/image/upload/v1690807779/nsfw_placeholders/cartoon_of_shocked_hamster_shocked_facial_expression_whimsical_cartoon__tyyjgi.jpg",
        "https://res.cloudinary.com/dzkwltgyd/image/upload/v1690807782/nsfw_placeholders/cartoon_of_a_hamster_with_hands_in_face_in_shame_cute_whimsical_1970s_cartoon_iapc3o.jpg",
    ]:
        raise NSFWError

    return image_url


#
# BOT LOGIC
#

global_reaction_watchlist = deque(maxlen=1000)
reactors = [
    BackgroundRemoverReactor(),
    AvatarRemixReactor(),
    MannyCardReactor(),
    PromptExplorerUpReactor(),
    PromptExplorerDownReactor(),
    PromptExplorerLeftReactor(),
    PromptExplorerRightReactor(),
]
for reactor in reactors:
    reactor.set_glif_client(glif_client)


async def add_reactions(message, reactors, collection: Optional[str] = None):
    # add reactions
    if collection == "mannygen":
        await message.add_reaction("<:mannykekw:960995341715517460>")
        await message.add_reaction("<:mannypog:960999842522468403>")
        await message.add_reaction("<:mannymonkaS:961004032556679189>")
    for reactor in reactors:
        if collection is not None and reactor.collection != collection:
            continue
        await message.add_reaction(reactor.emoji)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

    latest_nth = await get_len()
    for reactor in reactors:
        if hasattr(reactor, "nonce"):
            reactor.nonce = latest_nth + 1
            print(f"🃏: set nonce of cardmaker to {reactor.nonce}")


@client.event
async def on_message(message: Message):
    """React to messages."""
    if message.author == client.user:
        return

    if check_manny_command(message):
        try:
            placeholder_message = await message.channel.send(
                content="https://media1.tenor.com/images/7cc288921752b1a3dd2383d4c90bda0b/tenor.gif?itemid=27328551",
                reference=message,
            )
            image_url = await generate_manny_image(message.content)
            await placeholder_message.delete()
            new_message = await message.channel.send(
                content=image_url,
                reference=message,
            )

            await add_reactions(new_message, reactors, collection="mannygen")
            # add to reaction_watchlist
            global_reaction_watchlist.append(
                WatchlistTuple(
                    id=new_message.id, prompt=message.content, collection="mannygen"
                )
            )
        except NSFWError:
            print("[red] nsfw error")
            await placeholder_message.edit(
                content="<:mannydead:965319045559754772> (nsfw triggered)"
            )
        except Exception as e:
            print(f"[red] {e}")
            message = await placeholder_message.edit(
                content="<:mannydead:965319045559754772>"
            )

    if check_promptexplorer_command(message):
        placeholder_message = await message.channel.send(
            content="https://media1.tenor.com/images/7cc288921752b1a3dd2383d4c90bda0b/tenor.gif?itemid=27328551",
            reference=message,
        )
        location = message.content.replace("!explore ", "")
        output = await glif_client.arun_simple(
            "clv3pw40z00002rrjxlurnzjr",
            {"direction": "start", "location": location},
        )
        output = json.loads(output)
        await placeholder_message.delete()
        new_message = await message.channel.send(
            content=output["image_url"],
            reference=message,
        )

        await add_reactions(new_message, reactors, collection="prompt_explorer")

        # add to reaction_watchlist
        global_reaction_watchlist.append(
            WatchlistTuple(
                id=new_message.id, prompt=location, collection="prompt_explorer"
            )
        )


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    # check if we can find a ref in the watchlist
    watchlist_tuple = None
    for wt in global_reaction_watchlist:
        if wt.id == reaction.message.id:
            watchlist_tuple = wt
            break
    if watchlist_tuple is None:
        print("watchlist_tuple is None, returning")
        return

    context = ReactorContext(
        message=reaction.message,
        user=user,
        reaction_watchlist=global_reaction_watchlist,
    )

    for reactor in reactors:
        # only run reactors that are in the same collection
        if (
            watchlist_tuple.collection is not None
            and reactor.collection != watchlist_tuple.collection
        ):
            continue
        if str(reaction.emoji) == reactor.emoji:
            try:
                reactor_result = await reactor.run(context)

                if reactor_result is None:
                    print("reactor_result is None, returning")
                    return

                if reactor_result.content is None:
                    print("reactor_result.content is None, returning")
                    return
                new_message = await reaction.message.channel.send(
                    content=reactor_result.content,
                    reference=reaction.message,
                )
                if reactor_result.add_to_watchlist:
                    global_reaction_watchlist.append(
                        WatchlistTuple(
                            id=new_message.id,
                            prompt=reactor_result.prompt,
                            collection=reactor.collection,
                        )
                    )
                    await add_reactions(
                        new_message, reactors, collection=reactor.collection
                    )
                    print(global_reaction_watchlist)
            except Exception as e:
                print(f"[red] {e}")
                raise e
            return


if __name__ == "__main__":
    client.run(Config.DISCORD_TOKEN)
