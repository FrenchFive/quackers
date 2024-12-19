# 🦆🤖 // QUACKERS

## DISCORD DUCK [BOT]

A discord bot in Python with a lot of functionalities. 


### FEATURES :
- 🐤 || **GENERAL** Features :
  - `/duck` : Send a Duck Picture
  - `/info` : Send an image with information about a user
  - Quackers repond to Mention and Replies with his personnality using :: **GPT4-TURBO** Model by OpenAI
- 👨🏻‍💻 || **Admin Functions** <sub>[Allows Admins to change value for the bot]</sub>
  - `/admin-add` : Add QuackCoins for a specific User to the Quack Database
  - `/admin-remove` : Remove QuackCoins for a specific User to the Quack Database
  - `/admin-logs` : Display the latest logs from Quackers to troubleshoot some errors
- 🪙 || **Coins** <sub>[Manage Coins earned on Discord]</sub>
  - `/coins` : Display how much coins the user has
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

> [!TIP]
> It is not necessary but **strongly** recommended.
> It allows the use of librairies in a specific configuration, meaning not breaking other code on other projects.

```bash
git clone https://github.com/FrenchFive/quackers.git
```

Navigate into the project directory:

```bash
cd quackers
```

#### 2. Create a Virtual Environment (Optional but Recommended)
Create a virtual environment to isolate dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 3. Install Dependencies
Install the required Python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### RUNNING THE BOT:

#### 1. Configure the `secret.env` File
Quackers uses a file named `secret.env` to store all secret keys. This file should not be shared.

Example structure for `secret.env`:

```txt
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (OPENAI Key)
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (DISCORD Key)
```

- Generate an **OpenAI API Key** [here](https://platform.openai.com/settings).
- Get your **Discord Bot Token** by navigating to the [Discord Developer Portal](https://discord.com/developers/docs/intro) and enabling necessary bot permissions.

---

#### 2. Configure the server to monitor

Modify the following code inside ```main.py```

```python
# Server IDs
serverid = [1159282148042350642, 945445171670171668]
testid = [1159282148042350642]
afkchannellist = ["afk"]
``` 

It should match the server your [Server ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)
> [!NOTE]
> Specifying the server is not something mendatory (ex: It is something youll avoid when sharing your bot to unknowm servers)
> BUT it makes adding or changing commands appear instantly into the specified servers (It is also great to control which server has access to what command (Especially when testing))

---

#### 3. Start the Bot
Run the bot script:

```bash
python bot.py
```

For additional support, open an issue in the [GitHub repository](https://github.com/FrenchFive/quackers/issues).

---

### CONTRIBUTION:

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

Enjoy using **Quackers**! 🦆

---

### IN WORK : 
- [ ] **Petting System** :
  - [ ] Testing the command to Approve for ALL
  - [x] Create Images
  - [ ] Create a Database for all accessories
    - [ ] Make a function to recreate the database when Quackers goes online based on the files in the folder
      - [ ] Make the ID unique and not change w/ time 
      - [ ] How to transmit information like price and name => Attach a file ? with information into it ?
  - [ ] Create a Database for Users and data about their pets
  - [ ] Create functions to interact with the pet :: Get info about level and xp ... etc .. 
  - [ ] Create a Training interaction : Make it gain level through training
    - [ ] Passive XP gain like earning coins while using the Discord
  - [ ] Create a Mission interaction 
  - [ ] Create functions to buy the pet and accessories [SHOP SYSTEM]
- [ ] **Crypto System** ?
- [ ] **Power on KAEDE** :: Kaede is a "Midjourney" like bot (that uses a lot of GPU and cannot afford to let it run all the time)
- [ ] Programmable messages for ADMIN
  - [ ] Making work programmed messages
  - [ ] Having an interface to see what is planned by admin 
  - [ ] Having messages to be sent once and some to be repeated every x amount of time
- [ ] GPT4-O
  - [ ] Rewrite the API python integration
  - [ ] Clean up what information is sent to OpenAi 
- [ ] Welcome Messages
  - [ ] Send a message to users when they join the server 
  - [ ] Making a personnalized message to user
  - [ ] Presentation 
    - [ ] Making a quick questionnaire to answer by user that would generate a message for presentation 
- [ ] Making a Discussion as logs on Github with the updates to keep track of the progress done 