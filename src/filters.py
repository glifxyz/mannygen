from discord import Message

from src.config import Config


def check_manny_command(message: Message) -> bool:
    if Config.DEV:
        if message.channel.id != Config.CHANNEL_GLIF_TEST:
            return False
    else:
        if message.channel.id != Config.CHANNEL_MANNY_ASKAI:
            return False

    content = message.content.lower()

    if not (content.startswith("!mg ") or content.startswith("!mannygen ")):
        return False

    # check if manny is in the sanitized content
    if "manny" not in content.replace("!mg ", "").replace("!mannygen ", ""):
        return False

    print("found manny command")

    return True


def check_manny_remix_command(message: Message) -> bool:
    if Config.DEV:
        if message.channel.id != Config.CHANNEL_GLIF_TEST:
            return False
    else:
        if message.channel.id != Config.CHANNEL_MANNY_ASKAI:
            return False

    content = message.content.lower()

    if not (content.startswith("!mg ") or content.startswith("!mannygen ")):
        return False

    # check if manny is in the sanitized content
    if " --img " not in content:
        return False

    print("found manny remix command")

    return True


def check_promptexplorer_command(message: Message) -> bool:
    if message.channel.id != Config.CHANNEL_GLIF_TEST:
        return False

    content = message.content.lower()

    if not content.startswith("!explore "):
        return False

    return True
