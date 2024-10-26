import discord
import asyncio
import os
from discord.ext import commands, tasks
from datetime import datetime, timedelta

# Define your bot's command prefix and intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True  # Necessary for tracking voice states
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Discord bot token not found. Please set the DISCORD_BOT_TOKEN environment variable.")

AUDIO_FILE_DIRECTORY = "./hour_sounds/"  # e.g., "audio_files/"
AUDIO_FILE_EXTENSION = ".mp3"  # Assuming .mp3 for each file
DEFAULT_AUDIO_FILE = "01.mp3"  # Default file to play if the current hour's file is missing

# Function to join and play the sound for the current hour
async def join_and_play_hourly_sound():
    current_hour = datetime.now().hour  # Get the current hour (0-23)
    audio_file_path = f"{AUDIO_FILE_DIRECTORY}{str(current_hour).zfill(2)}{AUDIO_FILE_EXTENSION}"

    # Check if the file exists; if not, use the default file
    if not os.path.exists(audio_file_path):
        audio_file_path = f"{AUDIO_FILE_DIRECTORY}{DEFAULT_AUDIO_FILE}"
    
    for guild in bot.guilds:
        voice_channels = guild.voice_channels
        if not voice_channels:
            continue

        # Find the most populated channel
        most_populated_channel = max(
            voice_channels, key=lambda channel: len(channel.members)
        )
        if len(most_populated_channel.members) == 0:
            continue

        # Connect to the channel and play the selected audio file
        voice_client = await most_populated_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(audio_file_path))

        # Wait until the audio finishes playing
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Disconnect from the channel
        await voice_client.disconnect()

# Schedule to run at the start of each hour
@tasks.loop(hours=1)
async def hourly_announcement():
    await join_and_play_hourly_sound()

@hourly_announcement.before_loop
async def before_hourly_announcement():
    await bot.wait_until_ready()

    # Calculate time until the next hour
    now = datetime.now()
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    wait_seconds = (next_hour - now).total_seconds()
    
    # Wait until the start of the next hour
    await asyncio.sleep(wait_seconds)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    hourly_announcement.start()
# Run the bot

bot.run(TOKEN)
