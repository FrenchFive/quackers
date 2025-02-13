# 🦆 Quackers - Installation & Setup Guide

Welcome to the **Quackers** installation guide! This document will help you set up and run the bot smoothly. 🚀

---

## 📌 Prerequisites
Before starting, ensure you have the following installed:

| Software  | Version       | Download Link |
|-----------|---------------|--------------|
| Python    | 3.12 or above | [Python.org](https://www.python.org/downloads/) |
| Git       | Latest        | [Git-scm.com](https://git-scm.com/downloads) |
| Terminal  | OS included   | - |

> **📝 Note:** The required Python modules are listed in `requirements.txt`.

---

## ⚙️ Installation Steps

### 1️⃣ Clone the Repository
First, clone the repository to your local machine using Git:

```bash
 git clone https://github.com/FrenchFive/quackers.git
```

Navigate into the project directory:

```bash
 cd quackers
```

---

### 2️⃣ Create a Virtual Environment (Recommended)
Setting up a virtual environment prevents dependency conflicts across projects.

#### 🐍 Using Python Virtual Environment:
```bash
python3 -m venv .venv
```

Activate the virtual environment:

- **Windows**:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source .venv/bin/activate
  ```

#### 🏗️ Using Conda:
```bash
conda create -n quackers python=3.12
conda activate quackers
```

---

### 3️⃣ Install Dependencies
Install all required libraries:
```bash
pip install -r requirements.txt
```

> **⚠️ Warning:** If you're using Python 3.13+, manually install `audioop-lts`:
> ```bash
> pip install audioop-lts
> ```

---

## 🚀 Running the Bot

### 1️⃣ Configure the `.env` File
The bot requires a `.env` file for API keys and configuration.
Create a `.env` file inside the project directory with the following content:

```ini
KEY_OPENAI=sk-proj-1234567890abcdefg
KEY_DISCORD=1234567890abcdefg
DISCORD_CLIENT_ID=12345678910
DISCORD_CLIENT_SECRET=KEY_123456789
DISCORD_REDIRECT_URI=http://127.0.0.1:5000/callback
FLASK_SECRET_KEY=supersecret
```

🔗 **Obtain API Keys:**
- [OpenAI API Key](https://platform.openai.com/settings)
- [Discord Bot Token](https://discord.com/developers/docs/intro)

---

### 2️⃣ Start the Bot
Run the bot script:
```bash
python backend/src/main.py
```

If everything is set up correctly, you should see output indicating the bot is running! ✅

---

## 🌐 Running the Web Server

### 1️⃣ Start the Flask Server
To monitor and configure the bot via the web interface, start the Flask server:

```bash
python web/main.py
```

### 2️⃣ Connect & Configure the Bot
1. Open the **Quackers Web Interface** (URL will be displayed in the terminal after running Flask).
2. **Log in with Discord.**
3. Select your **Discord Server**.
4. Configure settings using the sliders in the interface.

---

## 🛡️ Security & Good Practices
### 🔐 Set Bot Permissions in Discord
It is **strongly recommended** to configure permissions in Discord:

1. **Go to** `Server Settings` → `Integrations` → `Quackers`
2. Add **derogations** (exceptions) for all `/admin_...` commands.
3. **Restrict access** so `@everyone` cannot use admin commands.

---

## 🛠️ Troubleshooting

### 🔍 Common Issues & Fixes

| Issue  | Possible Fix |
|--------|-------------|
| `ModuleNotFoundError` when running `main.py` | Ensure dependencies are installed: `pip install -r requirements.txt` |
| Bot not responding in Discord | Check if the bot has permissions and is online in the server. |
| Flask server not starting | Ensure all environment variables are correctly set in `.env`. |

