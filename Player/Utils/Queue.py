"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

QUEUE = {}

import logging
logging.basicConfig(level=logging.INFO)

def add_to_queue(chat_id, search_results, songlink, stream_url):
    if chat_id in QUEUE:
        chat_queue = QUEUE[chat_id]
        chat_queue.append([chat_id, search_results, songlink, stream_url])
        return len(chat_queue) - 1
    else:
        QUEUE[chat_id] = [[chat_id, search_results, songlink, stream_url]]
        return 0 

def get_queue(chat_id):
    return QUEUE.get(chat_id, [])

def pop_an_item(chat_id):
    if chat_id in QUEUE and QUEUE[chat_id]:
        QUEUE[chat_id].pop(0)
        return 1
    return 0

def clear_queue(chat_id):
    if chat_id in QUEUE:
        QUEUE.pop(chat_id)
        return 1
    return 0

def process_next_song(chat_id):
    queue_data = get_queue(chat_id)
    if queue_data:
        next_song_data = queue_data[0]
        
        if len(next_song_data) == 4:
            chat_id, search_results, songlink, stream_url = next_song_data
            print(f"Processing next song: {songlink}")
        else:
            print(f"Invalid data in queue: {next_song_data}. Expected 4 elements.")
            logging.error(f"Invalid data in queue for chat_id {chat_id}: {next_song_data}")
    else:
        print(f"Queue is empty for chat_id: {chat_id}")
