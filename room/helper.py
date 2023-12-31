from random import randint

import openai
from enigma.settings import SECRET_OPENAI
import translators as ts


# api openai
openai.api_key = SECRET_OPENAI


def robot(chat):
    chatgpt_r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": chat},
        ]
    )
    return chatgpt_r


def create_random_upc():
    return randint(1000000000000000000, 9999999999999999999)


def text2img(chat):
    chat = translate(chat)
    chatgpt_r = openai.Image.create(
        prompt=chat,
        n=1,
        size="1024x1024"
    )
    return chatgpt_r


def translate(chat):
    result = ts.translate_text(chat, to_language='en')
    return result





