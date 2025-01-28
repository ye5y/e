import discord
import aiohttp
import asyncio
from discord.ext import commands

# Replace with your bot token and role ping ID
BOT_TOKEN = 'bot_token'  # Your bot token
ROLE_PING_ID = 'roleping_id'         # The role ID to ping
CHANNEL_ID = channel_id            # Replace with your channel ID
CHECK_INTERVAL = 2.5                         # Time interval in seconds between username checks

# List of usernames to check
usernames = [
    'z0xr',
    'axtoq',
    'jyhhs',
    'swnnh',
    'unruz',
    'mtn2',
    'xn2u',
]

# Tracks the state of each username
username_status = {}

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def check_username(session, username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data.get('code') == 0 and data.get('message') == 'Username is valid':
                return "valid"
            elif data.get('code') == 1 and data.get('message') == 'Username is already in use':
                return "taken"
        return "error"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)

    if not channel:
        print("Channel not found. Please ensure the channel ID is correct.")
        return

    async with aiohttp.ClientSession() as session:
        while True:
            for username in usernames:
                try:
                    status = await check_username(session, username)

                    if status == "valid":
                        if username_status.get(username) != "valid":
                            # Notify about the valid username
                            role_mention = f"<@&{ROLE_PING_ID}>"
                            await channel.send(f"{role_mention} {username} WENT VALID TAKEE!!")
                            username_status[username] = "valid"

                    elif status == "taken":
                        if username_status.get(username) == "valid":
                            # Notify that the username has been taken
                            await channel.send(f"{username} is now TAKEN.")
                            username_status[username] = "taken"

                except Exception as e:
                    print(f"Error checking username {username}: {e}")

                await asyncio.sleep(CHECK_INTERVAL)  # Wait 1 second between username checks

bot.run(BOT_TOKEN)
