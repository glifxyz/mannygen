from typing import Union


class NSFWError(Exception):
    pass


def prep_manny_prompt(raw_content: str) -> str:
    print(f"Received prompt: {raw_content}")
    parsed = raw_content.lower()
    parsed = parsed.replace("!mannygen ", "").replace("!mg ", "")
    parsed = parsed.replace(
        "manny person", "manny"
    )  # revert to baseline so we know what to expect
    parsed = parsed.replace("manny", "manny person")
    parsed = parsed.replace("mannies", "manny persons")
    print(f"Sending prompt: {parsed}")
    return parsed


def extract_url(text: str) -> Union[str, None]:
    for chunk in text.split(" "):
        if chunk.startswith("https://res.cloudinary"):
            return chunk
    return None
