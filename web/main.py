from flask import Flask, url_for, redirect, request, session, jsonify, render_template
import requests
import os
from dotenv import load_dotenv
import time

from . import database as db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Discord OAuth2 credentials
CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI')
BOT_TOKEN = os.getenv('KEY_DISCORD')
API_BASE_URL = "https://discord.com/api"

def check_access_token():
    # Redirect to the home page if no access token is in the session
    if "access_token" not in session:
        return redirect('/')

    access_token = session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Verify the token by calling the Discord API
    response = requests.get(f"{API_BASE_URL}/oauth2/@me", headers=headers)

    if response.status_code == 200:
        # Token is valid
        return True
    else:
        # Token is invalid or expired
        session.pop("access_token", None)  # Remove invalid token from the session
        return redirect('/')

def get_server_info(server_id):
    # Check session cache first
    server_cache = session.get("server_info")

    cache_timestamp = session.get("server_info_timestamp")
    now = time.time()

    if (
        server_cache
        and str(server_cache.get("id")) == str(server_id)
        and cache_timestamp
        and now - cache_timestamp < 600  # 600 seconds = 10 minutes
    ):
        return server_cache


    headers = {"Authorization": f"Bot {BOT_TOKEN}"}

    # Get server (guild) information
    guild_response = requests.get(f"{API_BASE_URL}/guilds/{server_id}", headers=headers)
    guild_data = guild_response.json()

    # Get channels
    channels_response = requests.get(f"{API_BASE_URL}/guilds/{server_id}/channels", headers=headers)
    channels_data = channels_response.json()

    # Get roles
    roles_response = requests.get(f"{API_BASE_URL}/guilds/{server_id}/roles", headers=headers)
    roles_data = roles_response.json()

    # Separate channels into text and voice
    if channels_data!=None:
        text_channels = [
            {"id": channel["id"], "name": channel["name"]}
            for channel in channels_data if channel["type"] == 0  # Type 0 is text channel
        ]

        voice_channels = [
            {"id": channel["id"], "name": channel["name"]}
            for channel in channels_data if channel["type"] == 2  # Type 2 is voice channel
        ]
    
    
    server_info = {
        "name": guild_data.get("name"),
        "id": guild_data.get("id"),
        "text_channels": text_channels,
        "voice_channels": voice_channels,
        "roles": [{"id": role["id"], "name": role["name"]} for role in roles_data if isinstance(role, dict)],
    }

    # Save to session
    session["server_info"] = server_info
    session["server_info_timestamp"] = now

    return server_info


@app.route('/')
def home():
    logged_in = "access_token" in session
    return render_template('index.html', logged_in=logged_in)

@app.route('/about')
def about():
    logged_in = "access_token" in session
    return render_template('about.html', logged_in=logged_in)

@app.route('/login')
def login():
    discord_oauth_url = f"{API_BASE_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email"
    return redirect(discord_oauth_url)

@app.route('/callback')
def callback():
    # Retrieve the authorization code
    code = request.args.get('code')
    if not code:
        return "No code received from Discord", 400

    # Exchange the authorization code for an access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(f"{API_BASE_URL}/oauth2/token", data=data, headers=headers)
    response_json = response.json()

    if "access_token" not in response_json:
        return "Failed to get access token", 400

    # Save the token in the session
    session["access_token"] = response_json["access_token"]

    # Get user information
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    user_response = requests.get(f"{API_BASE_URL}/users/@me", headers=headers)
    user_json = user_response.json()

    if "id" not in user_json:
        return "Failed to get user information", 400

    # Save the user ID in the session
    session["user_id"] = user_json["id"]

    return redirect('/')

@app.route('/servers', methods=['GET', 'POST'])
def servers():
    check_access_token()

    error = session.pop("error_message", None)
    
    access_token = session.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Fetch user's guilds information
    guilds_info = requests.get(f"{API_BASE_URL}/users/@me/guilds", headers=headers).json()

    # Fetch bot's guilds information
    bot_headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    bot_guilds_info = requests.get(f"{API_BASE_URL}/users/@me/guilds", headers=bot_headers).json()
    bot_guild_ids = {guild['id'] for guild in bot_guilds_info}

    # Function to check if the user has administrative permissions
    def is_admin(permissions):
        ADMIN_PERMISSIONS = 0x00000008  # Example value, adjust as necessary
        return (permissions & ADMIN_PERMISSIONS) == ADMIN_PERMISSIONS

    # Filter guilds where the user is the owner or has administrative permissions
    user_servers = []
    for guild in guilds_info:
        if guild['owner'] or is_admin(guild['permissions']):
            # Construct the icon URL
            if guild['icon']:
                guild['icon_url'] = f"https://cdn.discordapp.com/icons/{guild['id']}/{guild['icon']}.png"
            else:
                guild['icon_url'] = url_for('static', filename='data/imgs/placeholder.jpg')
            
            # Check if the bot is already on the server
            guild['bot_on_server'] = guild['id'] in bot_guild_ids
            
            user_servers.append(guild)

    user_servers = sorted(user_servers, key=lambda x: not x['bot_on_server'])

    logged_in = "access_token" in session
    return render_template('server.html', servers=user_servers, clientid=CLIENT_ID, error=error, logged_in=logged_in)

@app.route('/config/<int:server_id>')
def config(server_id):
    sv_check = db.server_check(server_id, get_server_info(server_id)["name"])
    if sv_check !=None:
        session["error_message"] = sv_check
        return redirect('/servers')
    check_access_token()
    server = get_server_info(server_id)
    data = db.get_server_info(server_id)
    logged_in = "access_token" in session
    return render_template('config-general.html', server=server, data=data, logged_in=logged_in)

@app.route('/config-welcome/<int:server_id>')
def config_welcome(server_id):
    sv_check = db.server_check(server_id, get_server_info(server_id)["name"])
    if sv_check !=None:
        session["error_message"] = sv_check
        return redirect('/servers')
    check_access_token()
    server = get_server_info(server_id)
    data = db.get_server_info(server_id)
    dm = db.get_txt("welcome_private")
    logged_in = "access_token" in session
    return render_template('config-welcome.html', server=server, data=data, dm=dm, logged_in=logged_in)

@app.route('/config-economy/<int:server_id>')
def config_economy(server_id):
    sv_check = db.server_check(server_id, get_server_info(server_id)["name"])
    if sv_check !=None:
        session["error_message"] = sv_check
        return redirect('/servers')
    check_access_token()
    server = get_server_info(server_id)
    data = db.get_server_info(server_id)
    logged_in = "access_token" in session
    return render_template('config-economy.html', server=server, data=data, logged_in=logged_in)

@app.route('/config-games/<int:server_id>')
def config_games(server_id):
    sv_check = db.server_check(server_id, get_server_info(server_id)["name"])
    if sv_check !=None:
        session["error_message"] = sv_check
        return redirect('/servers')
    check_access_token()
    server = get_server_info(server_id)
    data = db.get_server_info(server_id)
    logged_in = "access_token" in session
    return render_template('config-games.html', server=server, data=data, logged_in=logged_in)

@app.route('/config-ai/<int:server_id>')
def config_ai(server_id):
    sv_check = db.server_check(server_id, get_server_info(server_id)["name"])
    if sv_check !=None:
        session["error_message"] = sv_check
        return redirect('/servers')
    check_access_token()
    server = get_server_info(server_id)
    print(server)
    data = db.get_server_info(server_id)
    logged_in = "access_token" in session
    return render_template('config-ai.html', server=server, data=data, logged_in=logged_in)

@app.route('/save-config', methods=['POST'])
def save_config():
    # Retrieve JSON payload
    payload = request.json

    # Extract server_id and data from the payload
    server_id = payload.get("server_id")
    received_data = payload.get("data", [])
    
    # Ensure `received_data` is iterable and follows the expected structure
    for item in received_data:
        # Assuming `db.update_server_info` is a function that updates the database
        db.update_server_info(server_id, item["name"], item["value"])

    return jsonify({"success": True, "message": "Configuration updated successfully!"}), 200

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to home page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
