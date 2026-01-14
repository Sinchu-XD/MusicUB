"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import logging
logging.basicConfig(level=logging.INFO)

QUEUE = {}

# ─────────────────────────────
# ADD TO QUEUE
# ─────────────────────────────
def add_to_queue(chat_id, title, duration, stream_url, requested_by):
    if chat_id not in QUEUE:
        QUEUE[chat_id] = []

    QUEUE[chat_id].append(
        (title, duration, stream_url, requested_by)
    )

    logging.info(
        f"Added to queue | chat_id={chat_id} | total={len(QUEUE[chat_id])}"
    )
    return len(QUEUE[chat_id]) - 1


# ─────────────────────────────
# GET QUEUE
# ─────────────────────────────
def get_queue(chat_id):
    return QUEUE.get(chat_id, [])


# ─────────────────────────────
# POP CURRENT SONG
# ─────────────────────────────
def pop_an_item(chat_id):
    if chat_id in QUEUE and QUEUE[chat_id]:
        QUEUE[chat_id].pop(0)

        # 🔥 AUTO CLEAN IF EMPTY
        if not QUEUE[chat_id]:
            QUEUE.pop(chat_id, None)
            logging.info(f"Queue auto-cleared (empty) | chat_id={chat_id}")

        return 1
    return 0


# ─────────────────────────────
# CLEAR QUEUE (HARD CLEAR)
# ─────────────────────────────
def clear_queue(chat_id):
    if chat_id in QUEUE:
        QUEUE.pop(chat_id, None)
        logging.info(f"Queue cleared | chat_id={chat_id}")
        return 1
    return 0


# ─────────────────────────────
# PROCESS NEXT SONG (FOR VC)
# ─────────────────────────────
def process_next_song(chat_id):
    queue_data = get_queue(chat_id)

    if not queue_data:
        logging.info(f"Queue empty for chat_id {chat_id}")
        return None

    title, duration, stream_url, requested_by = queue_data[0]

    logging.info(
        f"Next Song → {title} | {duration} | Requested by {requested_by}"
    )

    return stream_url
