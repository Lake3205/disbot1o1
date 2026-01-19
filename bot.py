"""
Discord Bot Base
A simple Discord bot base using discord.py
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Discord bot token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot instance with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.members = True  # Required for member-related events

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Event that triggers when the bot successfully connects to Discord"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Game(name="!help for commands")
    )


@bot.event
async def on_member_join(member):
    """Event that triggers when a new member joins the server"""
    try:
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to the server!'
        )
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
    else:
        bot.run(TOKEN)
