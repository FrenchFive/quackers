# 🦆🤖 // QUACKERS

## DISCORD DUCK [BOT]

A discord bot in Python with a lot of functionalities. 


### FEATURES :
- 🐤 || **GENERAL** Features :
  - `/duck` : Send a Duck Picture
  - `/info` : Send an image with information about a user
  - Quackers repond to Mention and Replies with his personnality using :: **GPT4-TURBO** Model by OpenAI
- 👨🏻‍💻 || **Admin Functions** <sub>[Allows Admins to change value for the bot]</sub>
  - `/admin-scan` : Easy and quick bot setup
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

#### 2. Start the Bot
Run the bot script:

```bash
python bot.py
```

For additional support, open an issue in the [GitHub repository](https://github.com/FrenchFive/quackers/issues).

---

#### 3. Configure the server to monitor

Once the bot is launched and added to your discord channel, excecute the following /command in discord ```/admin_scan```

Answer all questions asked to personnalize your experience

```
Admin Role : The only role allowed to use "admin_..." /commands (except for "/admin_scan")
Newbie Role : The role assigned to New Members - allowing them access to "/presentation"
AFK Voice Channel : Voice Channel managed by discord - poeple going to this channel wont receive coins
General Channel : The main text channel of the server
Debugging Channel : Channel used to debug for dev 
Welcome Channel : Channel where Quackers will send Welcome Messages and Presentations from Members
Admin Info Channel : Channel used to share sensitive information to admin
```

For dev only - it is possible to access work-in-progress functions by modifying the `main.py`
<br><sub>`/admin_scan function displays the ID of the current server`</sub>
```python
# Server IDs
serverid = qdb.get_all_server_ids()
testid = [1159282148042350642] #server id for W.I.P functionnalities
``` 
It should match the server your [Server ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)


> [!NOTE]
> It is necessary to RESTART the bot once the /admin_scan has been done.
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
- [x] Welcome Messages
  - [ ] Generate a list of Welcome Messages with placeholder for the name 
  - [x] Tag the newbie
  - [x] Add Quackers emotes randomly (only positive emotes)
    - [ ] Add Quack Server custom emotes
    - [ ] Add more emotes/emojis
  - [ ] Send a message to users when they join the server 
  - [ ] Presentation 
    - [x] Make a presentation using Discord Commands
    - [x] Making a quick questionnaire to answer by user that would generate a message for presentation 
    - [ ] Use AI Gen to spice up the answers in Quackers style
- [ ] Making a Discussion as logs on Github with the updates to keep track of the progress done
- [ ] Make an UI for Admin to change some parameters of the BOT
- [x] Making a database for server
  - [x] Making a SETUP function to easly register and Update the server info
  - [ ] Having function display only the servers info and not global info (ex : Leaderboard of the server and not leaderboard of the bot)
  - [ ] Making a database / server using their id
- [ ] Find a way for Admin to see the DB for troubleshooting
- [ ] Add badges to INFO 
  - [ ] Admin Badge
  - [ ] Badge for newbies
  - [ ] Badge for the one here for a long time
  - [ ] Badge for Activity (Experience based)
  - [ ] Badge for boost
- [ ] Making an EXP system (hidden)
  - [ ] Exp cannot be reduced, used to see how Active are users
  - [ ] Give them rank as they become more active
  - [ ] Make progression exponential 
