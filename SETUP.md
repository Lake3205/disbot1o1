# Twitch Clip Monitor Setup Guide

## Prerequisites
1. A Discord bot token (you already have this)
2. A Twitch Developer account and application
3. A Discord channel named `clips-and-highlights` in your server

## Step 1: Create Twitch Application

1. Go to https://dev.twitch.tv/console/apps
2. Click "Register Your Application"
3. Fill in:
   - **Name**: Your bot name (e.g., "Discord Clip Bot")
   - **OAuth Redirect URLs**: `http://localhost` (required but not used)
   - **Category**: Choose "Application Integration"
4. Click "Create"
5. Click "Manage" on your new application

## Step 2: Get Your Credentials

Copy these values from your Twitch application:
- **Client ID**: Shows on the application page
- **Client Secret**: Click "New Secret" to generate one

## Step 3: Update .env File

Open your `.env` file and replace the placeholder values:

```env
TWITCH_CLIENT_ID=your_actual_client_id_here
TWITCH_CLIENT_SECRET=your_actual_client_secret_here
TWITCH_CHANNEL=your_twitch_username_here
```

**Important**: Use your Twitch username (login name), not display name!

## Step 4: Install Dependencies

Run this command in your terminal:
```bash
pip install -r requirements.txt
```

## Step 5: Create Discord Channel

In your Discord server, create a text channel named exactly: `clips-and-highlights`

## Step 6: Run the Bot

```bash
python bot.py
```

## How It Works

- The bot checks for new clips every 30 seconds
- When a new clip is created on your Twitch channel, it automatically posts to the Discord channel
- The message includes:
  - Clip title and link
  - Creator name
  - View count
  - Duration
  - Thumbnail preview

## Testing

1. Start the bot
2. Create a clip on your Twitch channel (or have a viewer create one)
3. Wait up to 30 seconds
4. Check your `clips-and-highlights` Discord channel

## Troubleshooting

**Bot doesn't post clips:**
- Verify your Twitch username is correct (login name, not display name)
- Check that the Discord channel name is exactly `clips-and-highlights`
- Ensure your bot has permission to post in that channel
- Check the console for error messages

**"Error: Twitch credentials not found":**
- Make sure you updated the `.env` file with your actual credentials
- No spaces around the `=` signs
- No quotes around the values

**Bot crashes:**
- Make sure you installed all dependencies: `pip install -r requirements.txt`
- Check that both Discord token and Twitch credentials are valid
