"""
This is a fastAPI app you can run with uvicorn src.app_explorer:app
"""

import textwrap

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.database import get_all_cards

app = FastAPI()

with open("assets/card_6.svg") as f:
    svg = f.read()

text_wrapper_action = textwrap.TextWrapper(width=50, max_lines=2, placeholder="...")
text_wrapper_footer = textwrap.TextWrapper(width=65, max_lines=2, placeholder="...")


def wrap_div(content):
    return f'<div class="transform transition duration-300 hover:scale-105" id="tilt-card">{content}</div>'


@app.get("/", response_class=HTMLResponse)
async def read_html():
    with open("html/cards_template.html") as f:
        cards_html = f.read()

    data = await get_all_cards()

    svgs = []
    for i, card_data in enumerate(data):
        move1_info = card_data.pop("move1_info")
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

        filled_svg = svg.format(**card_data)

        filled_svg = filled_svg.replace("894_497", str(i))

        svgs.append(wrap_div(filled_svg))

    html_content = cards_html.replace("{svgs}", "\n".join(svgs))

    return HTMLResponse(content=html_content, status_code=200)
