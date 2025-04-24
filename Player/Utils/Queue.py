"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


QUEUE = {}

def add_to_queue(chat_id, search_results, songlink, stream_url):
    data = [chat_id, search_results, songlink, stream_url]
    if chat_id not in QUEUE:
        QUEUE[chat_id] = []
    QUEUE[chat_id].append(data)
    return len(QUEUE[chat_id]) - 1

def get_queue(chat_id):
    return QUEUE.get(chat_id, [])

def pop_an_item(chat_id):
    if chat_id in QUEUE and QUEUE[chat_id]:
        QUEUE[chat_id].pop(0)
        if not QUEUE[chat_id]:
            QUEUE.pop(chat_id)
        return True
    return False

def clear_queue(chat_id):
    return QUEUE.pop(chat_id, None) is not None
