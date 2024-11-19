# Discord chat bot
This is a discord chat bot which i made for my discord channel, the bot can play music and give news from some specific youtube channels. I named this chat bot " Phóng viên Lê Hồng Quang " - The popular reporter in Vietnam, you can search for him on the google you are interested :)

## Installation
First, you have to clone the repository by: 
```bash
git clone https://github.com/HotPotatoes0210/Discord-Bot
```

install the requirements.txt :
```bash
pip install requirements.txt
```

## Usage

```python
import discord
from discord.ext import commands, tasks
import requests
import re
import yt_dlp
import asyncio
from datetime import datetime, timedelta

BOT_TOKEN = "PASTE YOUR DISCORD BOT TOKEN HERE"  # Discord Bot_Token
CHANNEL_ID = "YOUR DISCORD ROOM CHANNEL" #Discord Room Channel ID
FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}
CHECK_INTERVAL = 100 #Setting for the latest video within 10 minute late
```

Make sure to paste your bot_token and channel_id on the code so it can be connected to your discord bot 

After that you can run the server: 
```bash
python main.py
```

## Contributing
Pull requests are welcome. For major changes please open an issue first to discuss what you would like to change. Enjoy coding :)