"""
Web Server for Discord Bot Dashboard
Displays real-time command execution and bot statistics
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from datetime import datetime
from collections import deque
import threading
import json

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store command history (last 100 commands)
command_history = deque(maxlen=100)
bot_stats = {
    'total_commands': 0,
    'uptime': None,
    'guilds': 0,
    'users': 0,
    'status': 'offline'
}


@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')


@app.route('/api/commands')
def get_commands():
    """Get command history"""
    return jsonify(list(command_history))


@app.route('/api/stats')
def get_stats():
    """Get bot statistics"""
    return jsonify(bot_stats)


def log_command(command_data):
    """Log a command execution"""
    global bot_stats
    
    # Add timestamp
    command_data['timestamp'] = datetime.now().isoformat()
    
    # Add to history
    command_history.append(command_data)
    
    # Update stats
    bot_stats['total_commands'] += 1
    
    # Emit to all connected clients
    socketio.emit('new_command', command_data, namespace='/')
    
    print(f"Logged command: {command_data['command']}")


def update_bot_stats(stats):
    """Update bot statistics"""
    global bot_stats
    bot_stats.update(stats)
    socketio.emit('stats_update', bot_stats, namespace='/')


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('command_history', list(command_history))
    emit('stats_update', bot_stats)


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnect"""
    print('Client disconnected')


def run_server(host='0.0.0.0', port=5000):
    """Run the web server"""
    print(f"Starting web server on http://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    run_server()
