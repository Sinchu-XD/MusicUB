"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import json
import atexit
from Player.Utils.YtDetails import SearchYt

AUTOPLAY_STATE = {}
STATE_FILE = "autoplay_state.json"


# ─────────────────────────────
# AUTOPLAY TOGGLE
# ─────────────────────────────
async def autoplay(chat_id: int):
    AUTOPLAY_STATE[chat_id] = not AUTOPLAY_STATE.get(chat_id, False)
    return AUTOPLAY_STATE[chat_id]


async def is_autoplay_on(chat_id: int):
    return AUTOPLAY_STATE.get(chat_id, False)


# ─────────────────────────────
# GET RECOMMENDATION (YT MUSIC)
# ─────────────────────────────
async def get_recommendation(title: str):
    """
    Returns: (title, duration, stream_url) or None
    """
    try:
        search_results, stream_url = await SearchYt(f"{title} audio")
        if not search_results:
            return None

        song = search_results[0]
        return (
            song["title"],
            song["duration"],
            stream_url
        )
    except Exception:
        return None


# ─────────────────────────────
# SAVE / LOAD STATE
# ─────────────────────────────
def save_autoplay_state():
    with open(STATE_FILE, "w") as f:
        json.dump(AUTOPLAY_STATE, f)


def load_autoplay_state():
    global AUTOPLAY_STATE
    try:
        with open(STATE_FILE, "r") as f:
            AUTOPLAY_STATE = json.load(f)
    except Exception:
        AUTOPLAY_STATE = {}


load_autoplay_state()
atexit.register(save_autoplay_state)
