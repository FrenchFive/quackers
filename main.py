# -*- coding: utf-8 -*-
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from typing import Optional

from unidecode import unidecode

import openai
from datetime import datetime

import qdatabase as qdb
import games
import qdraw

import os
import random

import qlogs

import time
import requests

import re

scrpt_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = 'txt'
FOLDER_PATH = os.path.join(scrpt_dir, folder_name)

ENV = os.path.join(scrpt_dir, "secret.env")
with open(ENV, 'r') as env_file:
    env_data = env_file.readlines()
    KEY_OPENAI = env_data[0].strip()
    KEY_DISCORD = env_data[1].strip()

openai.api_key = KEY_OPENAI

LOGFILE = os.path.join(scrpt_dir, "qlogs.log")

bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

counter = 0

# Server IDs
serverid = [1159282148042350642, 945445171670171668]
testid = [1159282148042350642]
afkchannellist = ["afk"]


def context():
    global scrpt_dir

    # DELETE FILES
    try:
        files = openai.File.list()  # List all files
        for file in files['data']:
            if file['purpose'] == "fine-tune":  # Adjust purpose to match your use case
                openai.File.delete(file['id'])
    except Exception as e:
        print(f"Error while deleting files: {e}")

    # EXPORT DATABASE TO .json
    qdb.export()

    # ADD FILES
    try:
        for fi in os.listdir(FOLDER_PATH):
            filtmp = os.path.join(scrpt_dir, 'txt', fi)
            if os.path.getsize(filtmp) > 100:  # Skip files smaller than 100 bytes
                with open(filtmp, "rb") as f:
                    file_data = openai.File.create(file=f, purpose="fine-tune")  # Adjust purpose as needed
                    print(f"File uploaded: {file_data['id']}")
    except Exception as e:
        print(f"Error while uploading files: {e}")

    print('-- ALL FILES PROCESSED')


context()


def generate(prompt):
    messages = [
        {"role": "assistant", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or the model you want to use
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "I am having difficulties => see w/ Five"


# MODAL DISCORD
class BetCreation(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="BET CREATION",
            timeout=None,
        )

        self.bettitle = nextcord.ui.TextInput(
            label="BET TITLE",
            min_length=3,
            max_length=50,
        )
        self.add_item(self.bettitle)

        self.optionone = nextcord.ui.TextInput(
            label="OPTION 1 :",
            placeholder="YES",
            required=False,
            max_length=50,
        )
        self.add_item(self.optionone)

        self.optiontwo = nextcord.ui.TextInput(
            label="OPTION 2 :",
            placeholder="NO",
            required=False,
            max_length=50,
        )
        self.add_item(self.optiontwo)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        title = self.bettitle.value
        a = self.optionone.value if self.optionone.value else "YES"
        b = self.optiontwo.value if self.optiontwo.value else "NO"
        id = games.bet_create(interaction.user.name, title, a, b)
        view = ButtonMessage(id)

        mess = f"{interaction.user.name} initiated a bet : \n"
        mess += f"# **{title}** \n \n"
        mess += f"A: **{a}** \n"
        mess += f"B: **{b}**"
        await interaction.send(mess, view=view)


class ButtonMessage(nextcord.ui.View):
    def __init__(self, id):
        super().__init__()
        self.id = id

    @nextcord.ui.button(label=f"BET : A", style=nextcord.ButtonStyle.green)
    async def beta(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if qdb.user_in_db(interaction.user.name) == 0:
            qdb.add_user(interaction.user.name)
        if games.bet_status(self.id) == "open" and games.bet_has_betted(interaction.user.name, self.id) == 0:
            await interaction.response.send_modal(Betting(self.id, "A"))
            self.value = True
        else:
            await interaction.response.send_message("THIS BET HAS BEEN CLOSED", ephemeral=True)

    @nextcord.ui.button(label="BET : B", style=nextcord.ButtonStyle.blurple)
    async def betb(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if qdb.user_in_db(interaction.user.name) == 0 and games.bet_has_betted(interaction.user.name, self.id) == 0:
            qdb.add_user(interaction.user.name)
        if games.bet_status(self.id) == "open":
            await interaction.response.send_modal(Betting(self.id, "B"))
            self.value = True
        else:
            await interaction.response.send_message("THIS BET HAS BEEN CLOSED", ephemeral=True)


class Betting(nextcord.ui.Modal):
    def __init__(self, id, option):
        super().__init__(
            title="BETTING",
            timeout=None,
        )
        self.id = id
        self.option = option

        self.amount = nextcord.ui.TextInput(
            label="AMOUNT",
            placeholder="100",
            min_length=1,
            max_length=50,
        )
        self.add_item(self.amount)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            amount = int(self.amount.value)
        except ValueError:
            await interaction.send('Amount must be a number', ephemeral=True)
            return

        if amount > 0:
            if qdb.qcheck(interaction.user.name, amount) == 0:
                games.bet_join(self.id, interaction.user.name, amount, self.option)
                qdb.add(interaction.user.name, (amount * -1))
                await interaction.send(f"Confirming Joining Bet : {self.option}, with : {amount} QuackCoins", ephemeral=True)
            else:
                await interaction.send(f'{interaction.user.mention} do not have enough QuackCoins', ephemeral=True)


@bot.event
async def on_ready():
    qlogs.info("QUACKERS IS ONLINE")


# COMMANDS
@bot.slash_command(name="daily", description="Receive daily QuackCoins.", guild_ids=serverid)
async def daily(interaction: Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    result = qdb.daily(interaction.user.name)
    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(result)


@bot.slash_command(name="send", description="Send QuackCoins to someone.", guild_ids=serverid)
async def send(interaction: Interaction, amount: int, user: nextcord.Member):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    if qdb.user_in_db(user.name) == 0:
        qdb.add_user(user.name)

    result = qdb.send(interaction.user.name, user.name, amount)
    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(result)


@bot.slash_command(name="coins", description="Gives you your QuackCoins balance.", guild_ids=serverid)
async def coins(interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
    name = user.name if user else interaction.user.name
    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    result = qdb.coins(name)
    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(result)


@bot.slash_command(name="info", description="Get an Image of your Quack Profile", guild_ids=serverid)
async def info(interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
    if user is None:
        name = interaction.user.name
        url = interaction.user.display_avatar.url
    else:
        name = user.name
        url = user.display_avatar.url

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    await interaction.response.defer()

    result, rank = qdb.info(name)
    qdb.add(interaction.user.name, 5)

    path = qdraw.info(name, url, result, rank)

    imgfile = nextcord.File(path)
    await interaction.followup.send(file=imgfile)


@bot.slash_command(name="leaderboard", description="Display the Top.10 of the server", guild_ids=serverid)
async def leaderboard(interaction: Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    intro = "HERE IS A LEADERBOARD OF THE CURRENT STATE OF THE QUACK COINS // \n"
    results = qdb.leaderboard()
    result = '\n'.join(results)
    message = intro + result

    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(message)


@bot.slash_command(name="duck", description="Send a cute pic", guild_ids=serverid)
async def duck(interaction: Interaction):
    response = requests.get("https://random-d.uk/api/v2/random").json()
    url = response["url"]
    await interaction.response.send_message(url)


# GAMES
@bot.slash_command(name="dices", description="Gamble QuackCoins against Quackers by throwing dices.", guild_ids=serverid)
async def dices(interaction: Interaction, bet: Optional[int] = SlashOption(required=False), roll: Optional[int] = SlashOption(required=False)):
    bet = bet if bet else 100
    roll = roll if roll else 3
    amount = bet
    name = interaction.user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    if amount > 100:
        amount = 100
    if amount <= 0:
        amount = 1

    if roll > 10:
        roll = 10

    # CHECK MONEY
    money_check = qdb.qcheck(name, amount)

    if money_check == 0:
        intro = f"{name.upper()} vs QUACKERS \n {amount} QuackCoins on the table for {roll} rounds !!!\n" + ' \n'
        response, result = games.dices(roll, amount, name)
        response = intro + response

        if result == 0:
            amount *= -1
        elif result == 2:
            amount = 0

        qdb.add(name, amount)
        qdb.add(interaction.user.name, random.randint(0, 5))
    else:
        response = "Not enough QuackCoins"

    await interaction.response.send_message(response)


@bot.slash_command(name="rps", description="Gamble QuackCoins against Quackers by playing Rock Paper Scissors ...", guild_ids=serverid)
async def rps(
    interaction: Interaction,
    bet: int,
    element: int = SlashOption(
        name="picker",
        description="Pick something :",
        choices={"scissors": 0, "paper": 1, "rock": 2, "lizard": 3, "spock": 4},
    ),
):
    name = interaction.user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    if bet > 100:
        bet = 100
    if bet <= 0:
        bet = 1

    # CHECK MONEY
    money_check = qdb.qcheck(name, bet)

    if money_check == 0:
        result, mult = games.rps(element, bet, name)

        bet *= mult
        qdb.add(name, bet)
        qdb.add(interaction.user.name, random.randint(0, 5))
    else:
        result = "Not enough QuackCoins available."
    await interaction.response.send_message(result)


@bot.slash_command(name="8ball", description="Quackers gives answers to any questions. [YES or NO questions]", guild_ids=serverid)
async def eightball(interaction: Interaction, question: str):
    result = games.hball(interaction.user.name)
    message = f'> {interaction.user.name.capitalize()} asked : " *{question}* " \n {result}'
    qdb.add(interaction.user.name, random.randint(0, 5))
    await interaction.response.send_message(message)


# BETTING SYSTEM
@bot.slash_command(name="bet-create", description="Create a BET", guild_ids=serverid)
async def bet_create(interaction: nextcord.Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    if games.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_modal(BetCreation())
    else:
        await interaction.response.send_message('You already have a Bet going on. || send results of your bet before creating another one "/bet-result"', ephemeral=True)


@bot.slash_command(name="bet-close", description="Close a BET, users won't be able to bet on it.", guild_ids=serverid)
async def bet_close(interaction: nextcord.Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    if games.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_message('You do not have any bet going on', ephemeral=True)
    else:
        totala, totalb, totalbetter, totalbettera, totalbetterb, highest = games.bet_close(interaction.user.name)
        # GET INFO FROM THE BET
        await interaction.response.send_message('Status Updated', ephemeral=True)
        mess = "BET CLOSED !!! \n \n"
        mess += f"{totalbetter} Users entered the bet. \n"
        mess += f"A : **{totala}** QuackCoins by {totalbettera} user(s) \n"
        mess += f"B : **{totalb}** QuackCoins by {totalbetterb} user(s) \n"
        mess += f"The highest bet was by : {highest}"
        await interaction.send(mess)


@bot.slash_command(name="bet-result", description="Sends the money", guild_ids=serverid)
async def bet_result(
    interaction: Interaction,
    option: int = SlashOption(
        name="winner",
        description="Pick the winning option :",
        choices={"A": 0, "B": 1},
    ),
):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    if games.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_message('You do not have any bet going on', ephemeral=True)
    else:
        option = "A" if option == 0 else "B"
        games.bet_result(interaction.user.name, option)
        await interaction.response.send_message('MONEY SENT !!!')


# ADMIN
@bot.slash_command(name="admin-add", description="[ADMIN] add QuackCoins to a User", guild_ids=serverid)
async def admin_add(interaction: Interaction, amount: int, user: nextcord.Member):
    name = interaction.user.name
    user_name = user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    if qdb.user_in_db(user_name) == 0:
        qdb.add_user(user_name)

    qdb.add(user_name, amount)
    result = qlogs.admin(f"[ADMIN : {name}] ADDED {amount} <:quackCoin:1124255606782578698> to {user_name.upper()}")

    await interaction.response.send_message(result)


@bot.slash_command(name="admin-remove", description="[ADMIN] remove QuackCoins from a User", guild_ids=serverid)
async def admin_remove(interaction: Interaction, amount: int, user: nextcord.Member):
    name = interaction.user.name
    user_name = user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    if qdb.user_in_db(user_name) == 0:
        qdb.add_user(user_name)

    qdb.add(user_name, (amount * -1))
    result = qlogs.admin(f"[ADMIN : {name}] REMOVED {amount} <:quackCoin:1124255606782578698> from {user_name.upper()}")

    await interaction.response.send_message(result)


@bot.slash_command(name="admin-logs", description="[ADMIN] Retrieve last 5 lines from LOGS", guild_ids=serverid)
async def admin_logs(interaction: Interaction):
    try:
        # Read the last 5 lines from qlogs.log
        with open(LOGFILE, "r") as log_file:
            lines = log_file.readlines()[-5:]  # Get the last 5 lines

        # Send the lines as a code block
        formatted_lines = "".join(lines)
        await interaction.response.send_message(f"```\n{formatted_lines}\n```")
    except FileNotFoundError:
        await interaction.response.send_message("Error: qlogs.log file not found.")


# EVENTS
@bot.event
async def on_message(ctx):
    global counter
    if ctx.guild is None or ctx.author == bot.user:
        return

    if qdb.user_in_db(ctx.author.name) == 0:
        qdb.add_user(ctx.author.name)

    qdb.add_mess(ctx.author.name)

    #COIFFEUR
    pattern = re.compile(r"(?:^|\s)[qQ]+[uU]+[oO]+[iI]+[!? ]*(?:$|\s)")
    feurlist = ["FEUR","FEUR !!!","feur"]
    if bool(pattern.fullmatch(ctx.content)) == True:
        await ctx.channel.send(random.choice(feurlist))
        return

    if not bot.user.mentioned_in(ctx):
        await bot.process_commands(ctx)
        return

    qdb.add_quackers(ctx.author.name)
    counter += 1
    qlogs.info(f'{counter:02} // RESPONDING TO : {ctx.author.name}')

    prompt = ctx.content  # You can modify the prompt as needed

    message = unidecode(generate(prompt))

    chunk = 1800
    if len(message) < chunk:
        await ctx.channel.send(message)
    else:
        li_tosend = [message[i:i + chunk] for i in range(0, len(message), chunk)]
        for mess in li_tosend:
            await ctx.channel.send(mess)

    if counter >= 10:
        counter = 0
        qlogs.info("/// RESETTING COUNTER")
        context()


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # User connected to a voice channel
        if qdb.user_in_db(member.name) == 0:
            qdb.add_user(member.name)

        qdb.voiceactive(member.name)
        qdb.add(member.name, 15)
        qlogs.info(f"{member.name} is connected to a Voice Channel")

    if before.channel is None and after.channel.name in afkchannellist:
        # USER CONNECTED TO AFK
        if qdb.user_in_db(member.name) == 0:
            qdb.add_user(member.name)
        qlogs.info(f"{member.name} is detected AFK")
        qdb.voicestalled(member.name)

    if before.channel is not None and after.channel is None:
        # User disconnects
        if qdb.user_in_db(member.name) == 0:
            qdb.add_user(member.name)

        qdb.voicestalled(member.name)
        qlogs.info(f"{member.name} is disconnected")


bot.run(KEY_DISCORD)
