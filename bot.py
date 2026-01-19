"""
Discord Bot Base with Twitch Integration
A bot that monitors Twitch clips and posts them to Discord
"""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

# Load environment variables from .env file
load_dotenv()

# Get the Discord bot token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Get Twitch credentials
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_CHANNEL = os.getenv('TWITCH_CHANNEL')

# Create bot instance with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# Twitch API Helper Class
class TwitchAPI:
    """Helper class to interact with Twitch API"""
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.user_id = None
        
    async def get_access_token(self):
        """Get OAuth token from Twitch"""
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as resp:
                data = await resp.json()
                self.access_token = data.get('access_token')
                return self.access_token
    
    async def get_user_id(self, username):
        """Get Twitch user ID from username"""
        url = "https://api.twitch.tv/helix/users"
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {'login': username}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                data = await resp.json()
                if data.get('data'):
                    self.user_id = data['data'][0]['id']
                    return self.user_id
                return None
    
    async def get_clips(self, broadcaster_id, first=1):
        """Get recent clips for a broadcaster"""
        url = "https://api.twitch.tv/helix/clips"
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'broadcaster_id': broadcaster_id,
            'first': first
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                data = await resp.json()
                return data.get('data', [])


# Global Twitch API instance
twitch_api = None
last_clip_id = None


async def check_for_new_clips():
    """Background task to check for new clips"""
    global last_clip_id, twitch_api
    
    await bot.wait_until_ready()
    
    # Initialize Twitch API
    twitch_api = TwitchAPI(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    await twitch_api.get_access_token()
    await twitch_api.get_user_id(TWITCH_CHANNEL)
    
    print(f"Monitoring Twitch channel: {TWITCH_CHANNEL}")
    
    while not bot.is_closed():
        try:
            # Get most recent clip
            clips = await twitch_api.get_clips(twitch_api.user_id, first=1)
            
            if clips:
                latest_clip = clips[0]
                clip_id = latest_clip['id']
                
                # If this is a new clip we haven't seen
                if last_clip_id and clip_id != last_clip_id:
                    # Find the Discord channel
                    for guild in bot.guilds:
                        channel = discord.utils.get(guild.text_channels, name='clips-and-highlights')
                        if channel:
                            # Create embed for the clip
                            embed = discord.Embed(
                                title=latest_clip['title'],
                                url=latest_clip['url'],
                                description=f"Clipped by {latest_clip['creator_name']}",
                                color=discord.Color.purple()
                            )
                            embed.set_thumbnail(url=latest_clip['thumbnail_url'])
                            embed.add_field(name="Views", value=latest_clip['view_count'], inline=True)
                            embed.add_field(name="Duration", value=f"{latest_clip['duration']}s", inline=True)
                            embed.set_footer(text=f"Created: {latest_clip['created_at']}")
                            
                            await channel.send(f"🎬 New clip created!", embed=embed)
                            print(f"Posted clip: {latest_clip['title']}")
                
                last_clip_id = clip_id
        
        except Exception as e:
            print(f"Error checking clips: {e}")
        
        # Check every 30 seconds
        await asyncio.sleep(30)


@bot.event
async def on_ready():
    """Event that triggers when the bot successfully connects to Discord"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Game(name="!help for commands")
    )
    
    # Start the clip monitoring task
    bot.loop.create_task(check_for_new_clips())


@bot.event
async def on_member_join(member):
    """Event that triggers when a new member joins the server"""
    try:
        await member.send(f'Hi {member.name}, welcome to the server!')
    except discord.Forbidden:
        # User has DMs disabled from server members
        print(f"Could not send DM to {member.name} - DMs are disabled")


@bot.command(name='hello', help='Responds with a greeting')
async def hello(ctx):
    """A simple hello command"""
    await ctx.send(f'Hello {ctx.author.mention}!')


@bot.command(name='ping', help='Check bot latency')
async def ping(ctx):
    """Returns the bot's latency in milliseconds"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')


@bot.command(name='info', help='Display bot information')
async def info(ctx):
    """Displays information about the bot"""
    embed = discord.Embed(
        title="Bot Information",
        description="A simple Discord bot base",
        color=discord.Color.blue()
    )
    embed.add_field(name="Server Count", value=len(bot.guilds), inline=True)
    embed.add_field(name="User Count", value=len(bot.users), inline=True)
    embed.add_field(name="Prefix", value="!", inline=True)
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    """Global error handler for commands"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
        print(f"Error: {error}")


if __name__ == '__main__':
    if TOKEN is None:
        print("Error: DISCORD_TOKEN not found in environment variables.")
        print("Please create a .env file with your Discord bot token.")
        exit(1)
    elif TWITCH_CLIENT_ID is None or TWITCH_CLIENT_SECRET is None or TWITCH_CHANNEL is None:
        print("Error: Twitch credentials not found in environment variables.")
        print("Please add TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, and TWITCH_CHANNEL to your .env file.")
        exit(1)
    else:
        bot.run(TOKEN)
