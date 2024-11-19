#AUTHOR: TRAN DAI VIET HUNG
#Feel free to use my discord bot, I hope you guys like it :)

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

# Fetch YouTube video info
def fetch_youtube_info(channel_url):
    html = requests.get(channel_url + "/videos").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    video_id = re.search('(?<="videoId":").*?(?=")', html).group()
    video_url = "https://www.youtube.com/watch?v=" + video_id
    return info, video_url

# Channels to fetch news
vtv_channel = "https://www.youtube.com/@vtv24"
phegame_channel = "https://www.youtube.com/@daylaphegame"
namfang_channel = "https://www.youtube.com/@NamFang208"
valorant_channel = "https://www.youtube.com/@valorant"
info_vtv, url_vtv = fetch_youtube_info(vtv_channel)
info_phegame, url_phegame = fetch_youtube_info(phegame_channel)
info_namfang, url_namfang = fetch_youtube_info(namfang_channel)
info_valorant, url_valorant = fetch_youtube_info(valorant_channel)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

#Welcome message
@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Xin chào! Tao là phóng viên Lê Hồng Quang, mày gọi tao có chuyện gì ?")
lastest_vtv_video = None

#Getting news from VTV channel
@tasks.loop(seconds=CHECK_INTERVAL)
async def check_vtv_videos():
    global lastest_vtv_video
    try:
        info_vtv,url_vtv = fetch_youtube_info(vtv_channel)
        if(url_vtv!= lastest_vtv_video):
            lastest_vtv_video = url_vtv
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"Tin tức mới từ VTV: {info_vtv}\n{url_vtv}")
    except Exception as e:
        print(f"Error checking VTV channel: {e}")

#Getting news from PheGame channel
lastest_phegame_video = None
@tasks.loop(seconds=CHECK_INTERVAL)
async def check_phegame_video():
    global lastest_phegame_video
    try:
        info_phegame, url_phegame = fetch_youtube_info(phegame_channel)
        if(url_phegame != lastest_phegame_video):
            lastest_phegame_video = url_phegame
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"Tin tức mới về game từ PheGame: {info_phegame}\n{url_phegame}")
    except Exception as e:
        print(f"Error checking PheGame channel: {e}")

#This is getting news from my friend's youtube, he's a streamer. Subscribe him if you are interested :)
latest_namfang_video = None
@tasks.loop(seconds=CHECK_INTERVAL)
async def check_namfang_video():
    global latest_namfang_video
    try:
        info_namfang, url_namfang = fetch_youtube_info(namfang_channel)
        if(url_namfang != latest_namfang_video):
            latest_namfang_video = url_namfang
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"HỐLAAAAA Bà kon, NamFang vừa mới ra video mới kính mời mọi người vô xem ")
            await channel.send(f"{info_namfang}\n{url_namfang}")
    except Exception as e:
        print(f"Error checking NamFang208 channel: {e}")

#Getting news from Valorant channel
latest_valorant_video = None
@tasks.loop(seconds=CHECK_INTERVAL)
async def check_valorant_video():
    global latest_valorant_video
    try:
        info_valorant, url_valorant = fetch_youtube_info(valorant_channel)
        if(url_valorant != latest_valorant_video):
            latest_valorant_video = url_valorant
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"Tin tức mới về VALORANT")
            await channel.send(f"{info_valorant}\n{url_valorant}")
    except Exception as e:
        print(f"Error checking Valorant channel: {e}")

#Auto update alert
@bot.command()
async def game_auto(ctx):
    await ctx.send("Tin tức PheGame đã đước bật cập nhật tự động")
    await ctx.send("Nếu bạn muốn tắt tự động thông báo, vui lòng nhập lệnh !game_off")
    check_phegame_video.start()
@bot.command()
async def game_off(ctx):
    await ctx.send("PheGame đã tắt tự động thông báo, nếu muốn mở lại xin vui lòng nhập lệnh !game_auto")
    check_phegame_video.stop()
@bot.command()
async def news_auto(ctx):
    await ctx.send("Tin tức VTV đã đước bật cập nhật tự động")
    await ctx.send("Nếu bạn muốn tắt tự động thông báo, vui lòng nhập lệnh !news_off")
    check_vtv_videos.start()
@bot.command()
async def news_off(ctx):
    await ctx.send("VTV đã tắt tự động thông báo, nếu muốn mở lại xin vui lòng nhập lệnh !news_auto")
    check_vtv_videos.stop()
@bot.command()
async def namfang_stream(ctx):
    await ctx.send("Tin tức về Streamer NamFang sẽ được tự động cập nhật")
    check_namfang_video.start()
@bot.command()
async def valorant(ctx):
    await ctx.send("Tin tức mới về valorant sẽ được cập nhật tự động")
    check_valorant_video.start()
@bot.command()
async def valorant_off(ctx):
    await ctx.send("Tin tức về valorant đã tắt tự động thông báo")
    check_valorant_video.stop()
@bot.command()

#Send request to simsimi, this is a hilarious chatbot, feel free to use :)
async def sim(ctx,*,user_text):
    url = 'https://api.simsimi.vn/v1/simtalk'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'text': user_text, 'lc': 'vn', 'key': ''}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get('message', 'No message found')
        print("Phóng viên trả lời:", message)
        await ctx.send(f"{message}")
    else:
        print("Failed to get response. Status code:", response.status_code)
        print("Response:", response.text)

#Music bot class
class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

#Check whether user is in voice room or not
    @commands.command(pass_context = True)
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("Mày phải vô phòng voice thì tao mới mở nhạc cho mày chứ !!!")

        try:
            if ctx.voice_client is None:
                await voice_channel.connect()
                await ctx.send(f"Đã kết nối tới phòng voice: {voice_channel.name}") #Connected to voice room
                print(f"Đã kết nối tới phòng voice: {voice_channel.name}")
            elif ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)
                await ctx.send(f"Đã chuyển tới phòng voice: {voice_channel.name}") #Moving voice room
        except discord.Forbidden:
            return await ctx.send("Tao không có quyền để vô phòng voice này, hãy kiểm tra lại quyền của tao.") #Bot asks for the permission to join the voice room
        except discord.HTTPException as e:
            return await ctx.send(f"Đã xảy ra lỗi khi kết nối tới phòng voice: {e}") #Error exception 

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(f"ytsearch:{search}", download=False) #Youtube searching 
                    if 'entries' in info:
                        info = info['entries'][0]
                    url = info['url']
                    title = info['title']
                    self.queue.append((url, title))
                    await ctx.send(f'Thêm vô hàng chờ: **{title}**') #Add to the queue
                    print(f'Thêm vô hàng chờ: **{title}**')
                    if len(self.queue) > 1:
                        await ctx.send(f'Tổng cộng có {len(self.queue)} bài đang chờ') # Queue list
                    if not ctx.voice_client.is_playing():
                        await self.play_next(ctx)
                except Exception as e:
                    await ctx.send(f"Có lỗi ERROR: {str(e)}")

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
            if len(self.queue) >= 1:
                await ctx.send(f'Tổng cộng có {len(self.queue)} bài đang chờ') #Queue list
            await ctx.send(f'Đang chơi nhạc **{title}**') #Playing song 

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            if len(self.queue) >=1:
                await ctx.send("Qua bài khác") #Skiped song
            else:
                await ctx.send("Đã hết bài trong list nhạc") #End of songs in the list
            await self.play_next(ctx)
    async def check_voice_channel(self, ctx):
        if ctx.voice_client is not None:
            if len(ctx.voice_client.channel.members) == 1:  # Only the bot is in the voice channel
                await ctx.voice_client.disconnect()
                await ctx.send("Không còn ai nghe nhạc, tao out đây.")  #Timeout
async def main():
    async with bot:
        await bot.add_cog(MusicBot(bot))
        await bot.start(BOT_TOKEN)

asyncio.run(main())
