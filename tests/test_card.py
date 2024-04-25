from glif_client import GlifClient
import pytest
import json
from rich import print
import textwrap

glif_client = GlifClient()


@pytest.mark.asyncio
async def test_card():
    text_wrapper_action = textwrap.TextWrapper(width=50, max_lines=2, placeholder="...")
    text_wrapper_footer = textwrap.TextWrapper(width=65, max_lines=2, placeholder="...")

    prompt = "!mg manny as a firefighter"

    inputs = {
        "prompt": prompt.replace("!mg ", "").replace("!mannygen ", ""),
    }
    card_data = await glif_client.arun_simple("clumo1gze000ak7eymnp9z07j", inputs)

    try:
        card_data = json.loads(card_data)
    except Exception as e:
        raise Exception(f"[red] CardMaker failed parsing json, errror: {e}")

    print(f"cardmaker message content: {card_data}")

    move1_info = card_data.pop("move1_info")
    move1_info += "As a valiant protector of digital realms, Firefighting Manny bravely battles bugs and system failures. As a valiant protector of digital realms, Firefighting Manny bravely battles bugs and system failures."
    lines = text_wrapper_action.wrap(move1_info)
    if len(lines) == 1:
        move1_info_1 = lines[0]
        move1_info_2 = ""
    else:
        move1_info_1, move1_info_2, *_ = lines

    move2_info = card_data.pop("move2_info")
    lines = text_wrapper_action.wrap(move2_info)
    if len(lines) == 1:
        move2_info_1 = lines[0]
        move2_info_2 = ""
    else:
        move2_info_1, move2_info_2, *_ = lines

    footer = card_data.pop("footer")
    footer += "As a valiant protector of digital realms, Firefighting Manny bravely battles bugs and system failures. As a valiant protector of digital realms, Firefighting Manny bravely battles bugs and system failures."
    lines = text_wrapper_footer.wrap(footer)
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

    image_url = await glif_client.arun_simple(
        "clumtpbkq000011v8yedrk2en",
        {
            **card_data,
            "image_url": "https://res.cloudinary.com/dkpfhyd71-comfy/image/upload/v1712321042/glif-comfy/dcc8378d-868e-4e99-af81-c444eecd58ba.png",
            "nth": 400,
        },
    )

    print(f"cardmaker image url: {image_url}")
