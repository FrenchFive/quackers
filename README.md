# 🦆🤖 // QUACKERS

## DISCORD DUCK [BOT]

A discord bot in Python with a lot of functionalities. 


### FEATURES :
- 🐤 || **GENERAL** Features :
  - `/duck` : Send a Duck Picture
  - `/info` : Send an image with information about a user
  - `/presentation` : User answer few questions about themselves, used to know new members
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
- [ ] Making Admin Commands check for the roles in the db (except for admin scan if the server already is in the db)
- [ ] **Petting System** :
  - [x] Create Images
  - [ ] Create a Database for all accessories
    - [ ] Make a function to recreate the database when Quackers goes online based on the files in the folder
      - [ ] Make the ID unique and not change w/ time 
        - [ ] Read the ID from the json file, else write it from the Database or UUID
      - [ ] Have an info .json file for each image that contains all necessary info as name, price etc ...
  - [ ] Create a Database for Users and data about their pets
  - [ ] Interactions with PET
    - [ ] `/pet` to buy one or to have info about it
    - [ ] `/pet-train` to train your pet for 5 hours => earn more money
    - [ ] `/pet-mission` to send the pet search money for 2 hours => RANDOM (or accessory)
    - [ ] Make the pet have energy so it needs food to do more actions
      - [ ] Has 3 energy : Training takes 3 : Mission takes 1
      - [ ] Possibility to refill energy by feeding the pet => Cost money
  - [ ] Create functions to buy the pet and accessories [SHOP SYSTEM]
    - [ ] `/pet-shop` Access the shop to buy Chest to get items
      - [ ] Make it a Gatcha (random pull)
      - [ ] Make it possible to sell items 
    - [ ] `/pet-inventory` Sell items to get coins => not always worth it
      - [ ] List all accessories the user possess
        - [ ] Plus informations [ What position / Price / Rarity / Name ] 
      - [ ] Add buttons to equip or sell or send 
        - [ ] Equip / Unequip from the pet
        - [ ] Sell to get coins 
        - [ ] Send to another user
  - [ ] Make a role "pet" and have it display all functions except /pet => user buy a pet if doesnt have one already
- [ ] **Power on KAEDE** :: Kaede is a "Midjourney" like bot (that uses a lot of GPU and cannot afford to let it run all the time)
  - [ ] Or use OpenAI generation to generate image
- [ ] Programmable messages for ADMIN
  - [ ] Making work programmed messages
  - [ ] Having an interface to see what is planned by admin 
  - [ ] Having messages to be sent once and some to be repeated every x amount of time
- [x] GPT4-O
  - [x] Rewrite the API python integration
  - [x] Clean up what information is sent to OpenAi
  - [ ] Make it so short and long memory are dependant on the server and not global 
    - [ ] Transmit information about the server as server name and server context unique to each server 
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
  - [ ] Make progression exponentially hard
- [ ] Have different languages mapped to Quackers 
  - [ ] Making the default language English
- [ ] Remove `/admin-scan` scan Emojis for the server
  - [ ] Delete the column from the db
  - [ ] Make Quackers use custom emojis from each server
- [x] Bank Vault 
  - [x] Add debug to bank 
  - [x] `/bank` command displays the amount of coins in the bank // and the money to spend
    - [x] 2 Buttons : ADD (put money in the bank) // WITHDRAW (to get the money to spend) 
  - [x] Make user be able to give their coins to the bank to gain interest over them 
    - [x] 4% / month Updating every day => 0.14% / day 
- [ ] Make Integration to Social Media 
  - [ ] Make a Twitch Integration
  - [ ] Make a Youtube Integration
- [ ] Create Temporary Voice Channels ?? 
- [ ] Create Statistics about the server
  - [ ] Store Data
    - [ ] Message amount 
    - [ ] Voice amount
    - [ ] Number of members
  - [ ] Draw Curves
- [ ] Help Function
- [ ] Admin GiveAways 
- [ ] Modify the INFO to make the image more beautiful 
  - [ ] Switch to a dark Theme 
  - [ ] Make a moodboard of typos and styles 
    - [ ] Look into Frosted effects
- [x] Modifying the `/admin-scan`
  - [x] Add a function when doing `/scan` to correct the joining date on members 
  - [x] Make Adding new user automaticly have the right date
  - [x] Add a bot channel in the `/admin-scan`
- [ ] Use a better password env file system