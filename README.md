# 🦆🤖 // QUACKERS

## DISCORD DUCK [BOT]

A discord bot in Python with a lot of functionalities. 

[Discord](https://img.shields.io/badge/Quackers-WEBSITE-7289da?logo=discord&logoColor=white)
[![Discord](https://img.shields.io/badge/Discord-TEAM_QUACK-7289da?logo=discord&logoColor=white)](https://discord.gg/3NzqXTP8HG)
![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/github/license/FrenchFive/quackers)

### FEATURES :
- 🐤 || **GENERAL** Features :
  - `/duck` : Send a Duck Picture
  - `/info` : Send an image with information about a user
  - `/presentation` : User answer few questions about themselves, used to know new members
  - `/imagine` : Generate an Image using AI based on a prompt :: **DALL-E-3** Model by OpenAI
  - Quackers repond to Mention and Replies with his personnality using :: **GPT4-o** Model by OpenAI
- 👨🏻‍💻 || **Admin Functions** <sub>[Allows Admins to change value for the bot]</sub>
  - `/admin-scan` : Easy and quick bot setup
  - `/admin-add` : Add QuackCoins for a specific User to the Quack Database
  - `/admin-remove` : Remove QuackCoins for a specific User to the Quack Database
  - `/admin-logs` : Display the latest logs from Quackers to troubleshoot some errors
- 🪙 || **Coins** <sub>[Manage Coins earned on Discord]</sub>
  - `/coins` : Display how much coins the user has
  - `/bank` : Allows the user to store coins to get interest
  - `/send` : Send coins from a User to another
  - `/daily` : Receive Daily Coins everyday (with a Streak function, the more you do it, the more you get)
  - `/leaderboard` : Display the Top 10 Users with the most coins
- 🎲 || **Games** <sub>[Play Games and earn Coins]</sub>
  - `/dices` : Throw dices against Quackers, the one with the most points wins
  - `/rps` : Play Rock Paper Scissors Lizard Spoke with Quackers
  - `/8ball` : Answer any **YES/NO** question
  - `/bet-...` : Bet as much as you want against other Users to win a TON of Coins
    - `/bet-create` : Open a bet
    - `/bet-close` : Close all bets and Display info about the bet
    - `/bet-result` : Sends the money to the winners
- 😴 || **PASSIVE Actions** <sub>[Users are Rewarded for using the Discord Channel]</sub>
  - Messages : Each message sent through Discord gives a Coin
  - Voice Channel : Connecting to a Voice Channel gives some coins | Each hour spent on the Voice Channel gives more coins to the user
  - Welcome and Goodbye Messages : sends a Welcome Message // sends DM Message to new members
 
---

## INSTALLATION AND SETUP GUIDE

Welcome to **Quackers**, a bot designed to bring quacking fun to your projects! Follow the steps below to install and run the bot successfully.

---

### PREREQUISITES:
Before starting, ensure you have the following installed:

1. [Python](https://www.python.org/downloads/) (version 3.X).
2. [Git](https://git-scm.com/downloads).
3. A terminal or command-line interface.

Python Modules listed into : ```requirements.md```

---

### INSTALLATION STEPS:

## 📌 Quick Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/FrenchFive/quackers.git
cd quackers
```

### 2️⃣ Install Dependencies
#### 🐍 Using Virtual Environment (Recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate  # For Windows use: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a `.env` file with the necessary API keys:
```ini
KEY_OPENAI=your_openai_key
KEY_DISCORD=your_discord_bot_token
DISCORD_CLIENT_ID=your_client_id
DISCORD_CLIENT_SECRET=your_client_secret
DISCORD_REDIRECT_URI=http://127.0.0.1:5000/callback
FLASK_SECRET_KEY=your_secret_key
```

### 4️⃣ Start the Bot
```bash
python backend/src/main.py
```

### 5️⃣ Start the Flask Server for Web UI
```bash
python web/main.py
```

## 📖 Detailed Installation Guide
For more detailed installation steps, troubleshooting tips, and advanced configuration, refer to the **[Installation Guide](./docs/installation.md)**.


---

### CONTRIBUTION:

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

Enjoy using **Quackers**! 🦆

---

### IN WORK : 
For Active Development check the Dev Project 

- [ ] Programmable messages for ADMIN
  - [ ] Making work programmed messages
  - [ ] Having an interface to see what is planned by admin 
  - [ ] Having messages to be sent once and some to be repeated every x amount of time
- [ ] Making an EXP system (hidden)
  - [ ] Exp cannot be reduced, used to see how Active are users
  - [ ] Give them rank as they become more active
  - [ ] Make progression exponentially hard
- [ ] Have different languages mapped to Quackers 
  - [ ] Making the default language English
- [ ] Make Integration to Social Media 
  - [ ] Make a Twitch Integration
  - [ ] Make a Youtube Integration
  - [ ] Make it cost Quackcoins each message
- [ ] Create Temporary Voice Channels
- [ ] Help Function
  - [ ] Create a Support Ticket to get help
  - [ ] Send link to Wiki // or the config HTML
- [ ] Admin GiveAways 
- [ ] Have a Pet System
- [ ] Add Badges to Info Image
