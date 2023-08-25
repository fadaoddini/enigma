from random import randint

import openai
from enigma.settings import SECRET_OPENAI
import translators as ts


# api openai
openai.api_key = SECRET_OPENAI


def text2img(chat):
    chatgpt_r = openai.Image.create(
        prompt=chat,
        n=1,
        size="1024x1024"
    )
    return chatgpt_r


def translate(chat):
    result = ts.translate_text(chat, to_language='en')
    return result





