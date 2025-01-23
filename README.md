# 🦆🤖 // QUACKERS

## DISCORD DUCK [BOT]

A discord bot in Python with a lot of functionalities. 

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

---

### INSTALLATION STEPS:

#### 1. Clone the Repository
First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/FrenchFive/quackers.git
```

Navigate into the project directory:

```bash
cd quackers
```

#### 2. Create a Virtual Environment (Optional but Recommended)
Create a virtual environment to isolate dependencies:

> [!TIP]
> It is not necessary but **strongly** recommended.
> It allows the use of librairies in a specific configuration, meaning not breaking other code on other projects.

```bash
python3 -m venv .venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  .venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source .venv/bin/activate
  ```

#### 3. Install Dependencies
Install the required Python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### RUNNING THE BOT:

#### 1. Configure the `.env` File
Quackers uses a file named `.env` to store all secret keys. This file should not be shared.

Example structure for `.env`:

```txt
KEY_OPENAI=sk-proj-1234567890abcdefg
KEY_DISCORD=1234567890abcdefg
```

- Generate an **OpenAI API Key** [here](https://platform.openai.com/settings).
- Get your **Discord Bot Token** by navigating to the [Discord Developer Portal](https://discord.com/developers/docs/intro) and enabling necessary bot permissions.

A template of the file is available : `template.env`to help you create your `.env` file.

---

#### 2. Start the Bot
Run the bot script:

```bash
python backend/src/main.py
```

For additional support, open an issue in the [GitHub repository](https://github.com/FrenchFive/quackers/issues).

---

#### 3. Configure the server to monitor

Once the bot is launched and added to your discord channel, excecute the following /command in discord ```/admin-scan```

Answer all questions asked to personnalize your experience

```
Admin Role : The only role allowed to use "admin_..." /commands (except for "/admin-scan")
Newbie Role : The role assigned to New Members - allowing them access to "/presentation"
AFK Voice Channel : Voice Channel managed by discord - poeple going to this channel wont receive coins
General Channel : The main text channel of the server
Debugging Channel : Channel used to debug for dev 
Welcome Channel : Channel where Quackers will send Welcome Messages and Presentations from Members
Admin Info Channel : Channel used to share sensitive information to admin
```

For dev only - it is possible to access work-in-progress functions by modifying the `main.py`
<br><sub>`/admin-scan function displays the ID of the current server`</sub>
```python
# Server IDs
serverid = qdb.get_all_server_ids()
testid = [1159282148042350642] #server id for W.I.P functionnalities
``` 
It should match the server your [Server ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)


> [!NOTE]
> It is necessary to RESTART the bot once the /admin-scan has been done.
> This way the server will be added to the list of servers to use the commands.

---

#### 4. Good Practices

It is strongly recommended to go in DISCORD into :
Server SETTINGS // Integrations // Quackers

And "Add Derogations" to all `/admin_...` commands 
And not allow @everyone to use them

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
