import json
import asyncio
import atexit

AUTOPLAY_STATE = {}

async def autoplay(chat_id):
    if chat_id not in AUTOPLAY_STATE:
        AUTOPLAY_STATE[chat_id] = True
    AUTOPLAY_STATE[chat_id] = not AUTOPLAY_STATE[chat_id]
    return AUTOPLAY_STATE[chat_id]

async def is_autoplay_on(chat_id):
    return AUTOPLAY_STATE.get(chat_id, False)

def save_autoplay_state():
    with open("autoplay_state.json", "w") as f:
        json.dump(AUTOPLAY_STATE, f)

def load_autoplay_state():
    global AUTOPLAY_STATE
    try:
        with open("autoplay_state.json", "r") as f:
            AUTOPLAY_STATE = json.load(f)
    except FileNotFoundError:
        AUTOPLAY_STATE = {}

load_autoplay_state()

atexit.register(save_autoplay_state)
