# Hourly Announcer Discord Bot

This Discord bot joins the most populated voice channel in a server every hour to announce the time with a specific sound. Each hour can play a unique sound, and if no specific sound is set for an hour, it defaults to a preset sound file.

## Features

- Joins the most populated voice channel in the server at the start of each hour.
- Plays a specific sound file for each hour if available.
- Uses a default sound file if the specific hour's file is missing.
- Securely manages the bot token using environment variables.

## Requirements

- Python 3.8+
- `discord.py` library
- FFmpeg (for playing audio files in voice channels)

## Setup

### 1. Install Dependencies

First, install the required Python packages:

```
pip install discord.py
```

### 2. Install FFmpeg

FFmpeg is required to play audio files in Discord voice channels.

- Windows: Download from FFmpeg.org and add it to your PATH.
- macOS: Install via Homebrew:
    ```
    brew install ffmpeg
    ```
- Linux: Install via your package manager, e.g.:
    ```
    sudo apt update && sudo apt install ffmpeg
    ```

### 3. Set Up Environment Variables
For security, store your Discord bot token as an environment variable.
- Windows: Open Command Prompt and set the environment variable:
    ```
    setx DISCORD_BOT_TOKEN "YOUR_BOT_TOKEN_HERE"
    ```
- macOS/Linux: Open the terminal and set the environment variable:
    ```
    export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
    ```

### 4. Prepare Audio Files

Edit the directory for your hourly sound files and ensure each file follows this naming convention: `00.mp3`, `01.mp3`, ..., `23.mp3`, where `00.mp3` is for 12 AM, `01.mp3` for 1 AM, etc.

If an hour’s file is missing, the bot will default to `default.mp3`

## Running the Bot

To start the bot, run:
```
python bot.py
```

### Usage

The bot will:

- Automatically start joining and announcing the hour at the start of each hour.
- Join the most populated voice channel in the server and play the respective sound file.
- Disconnect after playing the sound.