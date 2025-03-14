import json
import os
from pyrogram import filters
from pyrogram.types import Message
from Player import app
from config import config


OWNER_ID = config.OWNER_ID

# Load or create sudo list
SUDO_FILE = "sudo_users.json"
if not os.path.exists(SUDO_FILE):
    with open(SUDO_FILE, "w") as f:
        json.dump({"sudo_users": []}, f)

# Load sudo users from file
with open(SUDO_FILE, "r") as f:
    SUDO_USERS = json.load(f)["sudo_users"]



# Function to save sudo users to file
def save_sudo_users():
    with open(SUDO_FILE, "w") as f:
        json.dump({"sudo_users": SUDO_USERS}, f)


# Middleware to check if user is authorized



# Add a sudo user
@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def add_sudo(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/addsudo user_id`")

    try:
        user_id = int(message.command[1])
        if user_id in SUDO_USERS:
            return await message.reply_text("⚠️ This user is already a sudo user!")
        
        SUDO_USERS.append(user_id)
        save_sudo_users()
        await message.reply_text(f"✅ Successfully added **{user_id}** as a sudo user.")
    except ValueError:
        await message.reply_text("❌ Invalid User ID. Must be a number.")


# Remove a sudo user
@app.on_message(filters.command("removesudo") & filters.user(OWNER_ID))
async def remove_sudo(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Usage: `/removesudo user_id`")

    try:
        user_id = int(message.command[1])
        if user_id not in SUDO_USERS:
            return await message.reply_text("⚠️ This user is not a sudo user!")
        
        SUDO_USERS.remove(user_id)
        save_sudo_users()
        await message.reply_text(f"✅ Successfully removed **{user_id}** from sudo users.")
    except ValueError:
        await message.reply_text("❌ Invalid User ID. Must be a number.")


# List sudo users
@app.on_message(filters.command("listsudo") & filters.user(OWNER_ID))
async def list_sudo(_, message: Message):
    if not SUDO_USERS:
        return await message.reply_text("ℹ️ No sudo users added yet.")
    
    sudo_list = "\n".join([f"- `{uid}`" for uid in SUDO_USERS])
    await message.reply_text(f"👑 **Sudo Users:**\n\n{sudo_list}")
  
