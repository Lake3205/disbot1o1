# Discord Bot Web Dashboard

A real-time web dashboard to monitor your Discord bot's command activity.

## Features

- **Real-time Command Monitoring**: See all commands as they're executed
- **Live Statistics**: Track total commands, guilds, users, and bot status
- **Beautiful Vue.js Interface**: Modern, responsive dashboard with smooth animations
- **WebSocket Updates**: Instant updates without page refresh
- **Command History**: View up to 100 most recent commands
- **Filter Options**: View all commands or just the 10 most recent

## Dashboard Preview

The dashboard displays:
- Bot online/offline status
- Total commands executed
- Number of guilds and users
- Real-time command feed with:
  - Command name
  - User who executed it
  - Guild and channel information
  - Timestamp
  - Command arguments (if any)

## Accessing the Dashboard

Once the bot is running, open your browser and navigate to:
```
http://localhost:5000
```

The dashboard will automatically connect via WebSocket and start displaying commands in real-time.

## Technical Details

- **Backend**: Flask with Flask-SocketIO for real-time communication
- **Frontend**: Vue 3 with native WebSocket support
- **Port**: 5000 (configurable in webserver.py)
- **Storage**: In-memory command history (last 100 commands)

## How It Works

1. When the bot starts, it launches the web server in a separate thread
2. The web dashboard connects via WebSocket
3. Every time a command is executed, the bot logs it to the webserver
4. The webserver broadcasts the command to all connected clients
5. The Vue frontend displays the command in real-time with animation

## Customization

You can customize the dashboard by editing:
- `templates/index.html` - Frontend UI and Vue.js logic
- `webserver.py` - Backend API and WebSocket handlers
- Port and host settings in bot.py's webserver startup
