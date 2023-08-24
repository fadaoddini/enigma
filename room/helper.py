from random import randint

import openai

from enigma.settings import SECRET_OPENAI

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






