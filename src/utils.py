from typing import Union


class NSFWError(Exception):
    pass


def extract_url(text: str) -> Union[str, None]:
    for chunk in text.split(" "):
        if chunk.startswith("https://res.cloudinary"):
            return chunk
    return None
