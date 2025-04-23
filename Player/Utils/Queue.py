QUEUE = {}

def add_to_queue(chat_id, title, duration, songlink, link):
    print(f"Adding to queue: {chat_id}, {title}, {duration}, {song_link}, {link}")
    try:
        if chat_id in QUEUE:
            chat_queue = QUEUE[chat_id]
        else:
            chat_queue = []
            QUEUE[chat_id] = chat_queue
        chat_queue.append([chat_id, title, duration, songlink, link])
        return len(chat_queue) - 1
    except Exception as e:
        print(f"Error adding to queue: {e}")
        return None

def get_queue(chat_id):
    try:
        if chat_id in QUEUE:
            return QUEUE[chat_id]
        else:
            return []
    except Exception as e:
        print(f"Error getting queue: {e}")
        return []

def pop_an_item(chat_id):
    try:
        if chat_id in QUEUE:
            chat_queue = QUEUE[chat_id]
            if chat_queue:
                chat_queue.pop(0)
                return 1
            else:
                return 0
        else:
            return 0
    except Exception as e:
        print(f"Error popping item from queue: {e}")
        return 0

def clear_queue(chat_id):
    try:
        if chat_id in QUEUE:
            QUEUE.pop(chat_id)
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Error clearing queue: {e}")
        return 0
