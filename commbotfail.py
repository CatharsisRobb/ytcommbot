import discord
import requests
import asyncio
from discord import Intents
from discord.ext import commands

# Replace with your Discord bot token and YouTube API key
DISCORD_TOKEN = 'BRUH'
YOUTUBE_API_KEY = 'WHY YOU PEAKIN?'
CHANNEL_ID = 'THESE ARENT SENSIIVE'  # YouTube channel ID to monitor
DISCORD_CHANNEL_ID = 'REMOVING THEM ANYWAY'  # Discord channel ID to post in

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

async def fetch_youtube_posts():
    url = f'https://www.googleapis.com/youtube/v3/communityPosts?part=snippet&key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}'
    response = requests.get(url)
    data = response.json()
    return data.get('items', [])

async def post_to_discord():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    last_post_id = None  # Store the last seen post ID to avoid duplicates

    while True:
        posts = await fetch_youtube_posts()
        if posts:
            for post in posts:
                post_id = post['id']
                if post_id != last_post_id:  # Check for new posts
                    last_post_id = post_id
                    content = post['snippet']['title']  # Adjust to get the desired content
                    await channel.send(content)
        await asyncio.sleep(600)  # Check every 10 minutes

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(post_to_discord())

bot.run(DISCORD_TOKEN)
