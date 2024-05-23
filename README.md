# 🦆🤖 // QUACKERS
## DISCORD DUCK [BOT]

A discord bot in Python with a lot of functionalities. 


### FEATURES :
- **GENERAL** Features :
  - `/duck` : Send a Duck Picture
  - `/info` : Send an image with information about a user
  - Quackers repond to Mention and Replies with his personnality using :: **GPT4-TURBO** Model by OpenAI
- 👨🏻‍💻 // **Admin Functions** <sub>[Allows Admins to change value for the bot]</sub>
  - `/admin-add` : Add QuackCoins for a specific User to the Quack Database
  - `/admin-remove` : Remove QuackCoins for a specific User to the Quack Database
  - `/admin-logs` : Display the latest logs from Quackers to troubleshoot some errors
- 🪙 // **Coins** <sub>[Manage Coins earned on Discord]</sub>
  - `/coins` : Display how much coins the user has
  - `/send` : Send coins from a User to another
  - `/daily` : Receive Daily Coins everyday (with a Streak function, the more you do it, the more you get)
  - `/leaderboard` : Display the Top 10 Users with the most coins
- 🎲 // **Games** <sub>[Play Games and earn Coins]</sub>
  - `/dices` : Throw dices against Quackers, the one with the most points wins
  - `/rps` : Play Rock Paper Scissors Lizard Spoke with Quackers
  - `/bet-...` : Bet as much as you want against other Users to win a TON of Coins
    - `/bet-create` : Open a bet
    - `/bet-close` : Close all bets and Display info about the bet
    - `/bet-result` : Sends the money to the winners
- 😴 // **PASSIVE Actions** <sub>[Users are Rewarded for using the Discord Channel]</sub>
  - Messages : Each message sent through Discord gives a Coin
  - Voice Channel : Connecting to a Voice Channel gives some coins | Each hour spent on the Voice Channel gives more coins to the user
 


### What should be next : 
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
- [ ] **Random Duck Image from the internet**
  - [x] Find a **FREE** Database or API
  - [x] Testing the command to Approve for ALL
- [ ] GPT4-O
  - [ ] Rewrite the API python integration
