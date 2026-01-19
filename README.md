# disbot1o1

A simple Discord bot base built with Python and discord.py.

## Features

- Basic command handling with `!` prefix
- Event listeners (on_ready, on_member_join)
- Example commands:
  - `!hello` - Get a greeting from the bot
  - `!ping` - Check bot latency
  - `!info` - Display bot information
- Error handling for common command errors
- Easy to extend with more commands and features

## Prerequisites

- Python 3.8 or higher
- A Discord bot token (see setup instructions below)

## Setup

### 1. Get a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under the bot's username, click "Reset Token" and copy the token
5. Enable the following Privileged Gateway Intents:
   - MESSAGE CONTENT INTENT
   - SERVER MEMBERS INTENT

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Bot

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace `your_discord_bot_token_here` with your actual bot token:
   ```
   DISCORD_TOKEN=your_actual_token_here
   ```

### 4. Invite the Bot to Your Server

1. Go to the Discord Developer Portal
2. Select your application
3. Go to the "OAuth2" > "URL Generator" section
4. Select the following scopes:
   - `bot`
5. Select the following bot permissions:
   - Send Messages
   - Read Messages/View Channels
   - Read Message History
   - Embed Links
6. Copy the generated URL and open it in your browser
7. Select the server you want to add the bot to

## Running the Bot

```bash
python bot.py
```

You should see a message like:
```
BotName#1234 has connected to Discord!
Bot is in 1 guild(s)
```

## Available Commands

- `!hello` - Bot will greet you
- `!ping` - Check the bot's latency
- `!info` - Display bot information
- `!help` - Show all available commands (built-in discord.py command)

## Adding New Commands

To add a new command, use the `@bot.command()` decorator:

```python
@bot.command(name='mycommand', help='Description of my command')
async def my_command(ctx):
    await ctx.send('This is my custom command!')
```

## Project Structure

```
disbot1o1/
├── bot.py              # Main bot file with all the logic
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables file
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Troubleshooting

- **Bot doesn't respond to commands**: Make sure MESSAGE CONTENT INTENT is enabled in the Discord Developer Portal
- **Bot can't see members**: Enable SERVER MEMBERS INTENT in the Discord Developer Portal
- **Import errors**: Make sure you've installed all dependencies with `pip install -r requirements.txt`

## License

This project is open source and available for anyone to use and modify.
