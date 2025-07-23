"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


import os


API_ID: int = int(os.getenv("API_ID", 6067591))

API_HASH: str = os.getenv("API_HASH", "94e17044c2393f43fda31d3afe77b26b")

SESSION_STRING: str = os.getenv("SESSION_STRING", "BQBclYcAZZe_0_YNC3mOH2z2HnljeghVhYJtdRbsF7MgU7gBoqbKX0_W5HJdj4ba_gvGyEwKrkegiU6hJ38XjoIaIA69urDjjYZkWnzYtWdUcgeQkM0eKmCKanPdhz6Eqkg0D8s1kznoIFhW4T5N6yQ6DcXW7Q04GFEJRsNMSmPtNMdWWP_LXrb-WcpY4dvCkamUOw7ICqw4DPWXjtGdc36UHeClVy-DYmdVZfgipCZ50f7MirGXfb9Fx6mFqsuOYISEAx967XAZP2KRFUHV3bYHKzJDeDxB-6KQHRRazfpQGbf5WqxNbcdTTYHj2FM1GDue_75QJF05ueRQRoQh0OhRej6ghgAAAAHKUdR6AA")

OWNER_ID: list[int] = [int(os.getenv("OWNER_ID", 7862043458))]

MONGO_URL = os.getenv("MONGO_URI", "mongodb+srv://Music:Sinchu@cluster0.afnf5ch.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

LOG_GROUP_ID: int = int(os.getenv("LOG_GROUP_ID", -1002523755325))

PREFIX: str = str("/")

RPREFIX: str = str("-")



# No Need To Edit Below This

LOG_FILE_NAME: str = "Player.txt"
