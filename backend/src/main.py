# -*- coding: utf-8 -*-
import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from typing import Optional

from unidecode import unidecode

from datetime import datetime, timedelta

import qdatabase as qdb
import qgames
import qdraw
import qopenai
import qlogs
from consts import DATA_DIR, ROOT_DIR

import os
import random

import time
import requests

import re

import asyncio

from dotenv import load_dotenv
load_dotenv()

qlogs.clear()

TXT_PATH = os.path.join(DATA_DIR, 'txt')

KEY_DISCORD = os.getenv("KEY_DISCORD")

LOGFILE = os.path.join(ROOT_DIR, "qlogs.log")

bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

# Server IDs
serverid = qdb.get_all_server_ids()
testid = [1159282148042350642]

#check each db for server ids
for guild in serverid:
    qdb.servers_table_exists(guild)

def serv_list(li):
    if len(li) == 0:
        return [0]
    else:
        return li

# COMMANDS
@bot.slash_command(name="daily", description="Receive daily QuackCoins.", guild_ids = serv_list(list(set(qdb.get_server_list("dly")) & set(qdb.get_server_list("eco")))))
async def daily(interaction: Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    
    result = qdb.daily(interaction.guild.id, interaction.user.name)
    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    await interaction.response.send_message(result)


@bot.slash_command(name="send", description="Send QuackCoins to someone.", guild_ids= serv_list(list(set(qdb.get_server_list("snd")) & set(qdb.get_server_list("eco")))))
async def send(interaction: Interaction, amount: int, user: nextcord.Member):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    qdb.user_in_db(interaction.guild.id, user)

    result = qdb.send(interaction.guild.id, interaction.user.name, user.name, amount)
    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    await interaction.response.send_message(result)


@bot.slash_command(name="coins", description="Gives you your QuackCoins balance.", guild_ids=serv_list(qdb.get_server_list("eco")))
async def coins(interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    if user:
        qdb.user_in_db(interaction.guild.id, user)

    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))

    name = user.name if user else interaction.user.name
    result = qdb.coins(interaction.guild.id, name)
    
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    await interaction.response.send_message(result)


@bot.slash_command(name="info", description="Get an Image of your Quack Profile", guild_ids= serv_list(serverid))
async def info(interaction: Interaction, user: Optional[nextcord.Member] = SlashOption(required=False)):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    if user:
        qdb.user_in_db(interaction.guild.id, user)
    
    if user is None:
        name = interaction.user.name
        url = interaction.user.display_avatar.url
    else:
        name = user.name
        url = user.display_avatar.url

    await interaction.response.defer()

    result, rank = qdb.info(interaction.guild.id, name)
    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    path = qdraw.info(name, url, result, rank)

    imgfile = nextcord.File(path)
    await interaction.followup.send(file=imgfile)


@bot.slash_command(name="leaderboard", description="Display the Top.10 of the server", guild_ids= serv_list(qdb.get_server_list("eco")))
async def leaderboard(interaction: Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    intro = "HERE IS A LEADERBOARD OF THE CURRENT STATE OF THE QUACK COINS // \n"
    results = qdb.leaderboard(interaction.guild.id)
    result = '\n'.join(results)
    message = intro + result

    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    await interaction.response.send_message(message)


@bot.slash_command(name="duck", description="Send a cute pic", guild_ids= serv_list(serverid))
async def duck(interaction: Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    
    response = requests.get("https://random-d.uk/api/v2/random").json()
    url = response["url"]
    
    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)
    
    await interaction.response.send_message(url)

class PresentationModal(nextcord.ui.Modal):
    def __init__(self, target_channel, user, imgpath, questions, role, newbies):
        super().__init__(
            title="PRESENTATIONS",
            timeout=None,
        )

        self.interaction = user
        self.role = role
        self.newbies = newbies
        self.target_channel = target_channel  # Save the target channel ID
        self.user = user.name
        self.img = imgpath
        self.questions = questions

        # Questions
        self.pronouns = nextcord.ui.TextInput(
            label="Pronouns",
            placeholder="He/Him, She/Her, They/Them, ...",
            required=True,
        )
        self.add_item(self.pronouns)

        self.question1 = nextcord.ui.TextInput(
            label=self.questions[0][0],
            placeholder=self.questions[0][1],
            required=False,
        )
        self.add_item(self.question1)

        self.introduced_by = nextcord.ui.TextInput(
            label="Who introduced you to the server?",
            placeholder="Mention the user @username",
            required=True,
        )
        self.add_item(self.introduced_by)

        self.question2 = nextcord.ui.TextInput(
            label=self.questions[1][0],
            placeholder=self.questions[1][1],
            required=True,
        )
        self.add_item(self.question2)

        self.question3 = nextcord.ui.TextInput(
            label=self.questions[2][0],
            placeholder=self.questions[2][1],
            required=False,
        )
        self.add_item(self.question3)

    async def callback(self, interaction: nextcord.Interaction):
        # Dynamically generate a summary of the user's responses
        responses = [f"**Submitted By**: {self.user}"]

        if self.pronouns.value:
            responses.append(f"**Pronouns**: {self.pronouns.value}")
        if self.question1.value:
            responses.append(f"**{self.questions[0][0]}**: {self.question1.value}")
        if self.introduced_by.value:
            responses.append(f"**Introduced By**: {self.introduced_by.value}")
        if self.question2.value:
            responses.append(f"**{self.questions[1][0]}**: {self.question2.value}")
        if self.question3.value:
            responses.append(f"**{self.questions[2][0]}**: {self.question3.value}")
         
        # Send a thank-you message to the user
        await interaction.response.send_message(
            "Thank you for introducing yourself! Your responses have been recorded.",
            ephemeral=True,
        )

        qdb.add(interaction.guild.id, self.user, 300)

        #removing the role NEWBIE
        await self.interaction.remove_roles(self.role, reason="Role removed after presentation completion.")
        qlogs.info(f"Role '{self.role.name}' removed from {self.user}.")

        embed = nextcord.Embed(
            title=f"🎉 Welcome {self.user} to the Server! 🎉",
            description="Here's their introduction!",
            color=nextcord.Color.random(),
        )

        # Send the combined message to the target channel
        if responses:
            response_message = "\n".join(responses)
            gen_pres = qopenai.welcome(response_message)
            embed.add_field(name="Presentation", value=gen_pres, inline=False)
            target_channel = interaction.guild.get_channel(self.target_channel)
            if target_channel:
                with open(self.img, 'rb') as img_file:
                    file = nextcord.File(img_file, filename="thumbnail.png")
                    embed.set_thumbnail(url=f"attachment://thumbnail.png")
                    await target_channel.send(embed=embed, file=file)
            else:
                print(f"Error: Channel {self.target_channel} not found.")

@bot.slash_command(name="presentation", description="Introduce yourself to the server!", guild_ids= serv_list(qdb.get_server_list("prst")))
async def introduce(interaction: nextcord.Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    guild = interaction.guild
    role_new = qdb.get_server_info(guild.id, "prst_role")
    role = guild.get_role(role_new)
    if role is None:
        await interaction.response.send_message(
            "Required role not found in the server.",
            ephemeral=True,
        )
        return

    user_roles = interaction.user.roles
    has_required_role = any(urole.id == role.id for urole in user_roles)
    if not has_required_role:
        await interaction.response.send_message(
            "You do not have the required role to use this command.",
            ephemeral=True,
        )
        return

    url = interaction.user.display_avatar.url
    imgpath = qdraw.avatar_download(url)

    #get 3 random questions from introduction
    with open(os.path.join(TXT_PATH, "presentation.txt"), "r") as file:
        questions = file.readlines()
    introduction = []
    for question in questions:
        tmp = [item.strip() for item in question.split("//")]
        introduction.append((tmp[0],tmp[1]))
    random_questions = random.sample(introduction, 3)

    channel_welcome = qdb.get_server_info(interaction.guild.id, "wlc_ch_id")
    await interaction.response.send_modal(PresentationModal(target_channel=channel_welcome, user=interaction.user, imgpath=imgpath, questions=random_questions, role=role, newbies=role_new))  


class AmountModal(nextcord.ui.Modal):
    def __init__(self, user_name, action, base_m, message):
        super().__init__(title=f"AMOUNT to {['ADD', 'WITHDRAW'][action]}")
        self.user_name = user_name
        self.action = action
        self.base_m = base_m
        self.message = message

        # Number input field
        self.amount_input = nextcord.ui.TextInput(
            label="Enter the amount",
            placeholder="Type a number...",
            min_length=1,
            required=True
        )
        self.add_item(self.amount_input)

    async def callback(self, interaction: nextcord.Interaction):
        # Get the entered amount
        data = self.amount_input.value

        #convert amount to numbers
        amount = int(data) if data.isdigit() else 0
        if amount < 0:
            amount = 0

        coins, bank = qdb.bank(interaction.guild.id, self.user_name)

        match self.action:
            case 0:
                if amount > coins:
                    amount = coins
                response = qdb.bank_deposit(interaction.guild.id, self.user_name, amount)
            case 1:
                if amount > bank:
                    amount = bank
                response = qdb.bank_withdraw(interaction.guild.id, self.user_name, amount)
            case _:
                response = "Invalid action"
        
        coins, bank = qdb.bank(interaction.guild.id, self.user_name)

        update = str(self.base_m)
        update = update.replace("{name}", self.user_name.upper())
        update = update.replace("{coins}", str(coins))
        update = update.replace("{bank}", str(bank))
        await self.message.edit(content=update)

        # Send confirmation to the user
        await interaction.response.send_message(response, ephemeral=True)

class BankView(nextcord.ui.View):
    def __init__(self, user_name, base_m, message):
        super().__init__(timeout=60)  # Buttons will time out after 60 seconds
        self.user_name = user_name
        self.base_m = base_m
        self.message = message

    async def ensure_correct_user(self, interaction: nextcord.Interaction) -> bool:
        if interaction.user.name != self.user_name:
            await interaction.response.send_message(
                "🚫 You cannot use this menu. It belongs to someone else!",
                ephemeral=True
            )
            return False
        return True

    @nextcord.ui.button(label="Deposit", style=nextcord.ButtonStyle.green)
    async def add_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        qdb.user_in_db(interaction.guild.id, interaction.user)
        # Check if the user is the correct user
        if not await self.ensure_correct_user(interaction):
            return

        # Show the modal for adding coins
        await interaction.response.send_modal(AmountModal(self.user_name, action=0, base_m=self.base_m, message=self.message))

    @nextcord.ui.button(label="Withdraw", style=nextcord.ButtonStyle.red)
    async def withdraw_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        qdb.user_in_db(interaction.guild.id, interaction.user)
        # Check if the user is the correct user
        if not await self.ensure_correct_user(interaction):
            return

        # Show the modal for withdrawing coins
        await interaction.response.send_modal(AmountModal(self.user_name, action=1, base_m=self.base_m, message=self.message))

@bot.slash_command(name="bank", description="Interact with The Quackery Treasury", guild_ids= serv_list(list(set(qdb.get_server_list("bnk")) & set(qdb.get_server_list("eco")))))
async def bank(interaction: nextcord.Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    
    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    # Get the user's balance
    coins, bank = qdb.bank(interaction.guild.id, interaction.user.name)

    message = '''
    - 💷 THE QUACKERY TREASURY 💷 :: {name} -

    ------------------------------
    💰 **QuackCoins**: {coins} <:quackCoin:1124255606782578698>
    🏦 **BankCoins**: {bank} <:quackCoin:1124255606782578698>

    Current Interest Rate: 30% / month
    '''

    base_m = message
    message = message.replace("{name}", interaction.user.name.upper())
    message = message.replace("{coins}", str(coins))
    message = message.replace("{bank}", str(bank))

    # Send the initial message
    sent_message = await interaction.response.send_message(message)
    
    view = BankView(interaction.user.name, base_m, sent_message)
    await sent_message.edit(view=view)

class ImagineView(nextcord.ui.View):
    def __init__(self, user_name, prompt):
        super().__init__() 
        self.user_name = user_name
        self.prompt = prompt

    async def ensure_funds(self, interaction: nextcord.Interaction, price) -> bool:
        if qdb.qcheck(interaction.guild.id, interaction.user.name, price) == 1:
            await interaction.response.send_message(
                f"🚫 You do not have the money !  {price} Qc. are necessary",
                ephemeral=True
            )
            return False
        return True
    @nextcord.ui.button(label="Regenerate", style=nextcord.ButtonStyle.green, emoji="🔄")
    async def regenerate_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Check if the user is the correct user
        price = 100 #Will be changed to ask for DB / server price (not transmitted to check if the price has changed in the meantime)

        if not await self.ensure_funds(interaction, price):
            return

        # Regenerate the image
        qdb.add(interaction.guild.id, interaction.user.name, 5)
        qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)
        qdb.add(interaction.guild.id, interaction.user.name, -price)

        qlogs.info(f"{interaction.user.name} RE-GENERATING IMAGE :: {self.prompt}")
        img_path = qopenai.imagine(interaction.user.name, self.prompt)

        message = f"**{self.prompt[:100]}** :: by {interaction.user.mention}"

        view = ImagineView(interaction.user.name, self.prompt)
        await interaction.followup.send(content=message, file=nextcord.File(img_path), view=view)

    @nextcord.ui.button(label="Show Full Prompt", style=nextcord.ButtonStyle.blurple, emoji="📜")
    async def show_prompt_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Send the full prompt
        await interaction.followup.send(content=f"Full prompt: {self.prompt} by {interaction.user.name}")

@bot.slash_command(name="imagine", description="Cost : 100.Qc - Image generation using AI", guild_ids= serv_list(qdb.get_server_list("ai_img")))
async def imagine(interaction: nextcord.Interaction, prompt: str):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    await interaction.response.defer()  # Defer the response

    if qdb.get_server_info(interaction.guild.id, "ai_img_pay"):
        price = qdb.get_server_info(interaction.guild.id, "ai_img_pay_value")

        check = qdb.qcheck(interaction.guild.id, interaction.user.name, price)
        if check != 0:
            await interaction.followup.send("Not enough QuackCoins", ephemeral=True)
            return
        qdb.add(interaction.guild.id, interaction.user.name, -price)

    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
        qdb.add(interaction.guild.id, interaction.user.name, qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value"))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)

    qlogs.info(f"{interaction.user.name} GENERATING IMAGE :: {prompt}")
    img_path = qopenai.imagine(interaction.user.name, prompt)

    message = f"**{prompt[:100]}** :: by {interaction.user.mention}"

    view = ImagineView(interaction.user.name, prompt)
    await interaction.followup.send(content=message ,file=nextcord.File(img_path), view=view)


# qgames
@bot.slash_command(name="dices", description="Gamble QuackCoins against Quackers by throwing dices.", guild_ids= serv_list(list(set(qdb.get_server_list("dices")) & set(qdb.get_server_list("eco")) & set(qdb.get_server_list("game")))))
async def dices(interaction: Interaction, bet: Optional[int] = SlashOption(required=False), roll: Optional[int] = SlashOption(required=False)):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    bet = bet if bet else 100
    roll = roll if roll else 3

    if qdb.get_server_info(interaction.guild.id, "game_limit")==True and qdb.get_server_info(interaction.guild.id, "game_limit_value")>bet:
        amount = qdb.get_server_info(interaction.guild.id, "game_limit_value")
    else:
        amount = bet

    name = interaction.user.name

    if amount <= 0:
        amount = 1

    if roll > 10:
        roll = 10

    # CHECK MONEY
    money_check = qdb.qcheck(interaction.guild.id, name, amount)

    if money_check == 0:
        intro = f"{name.upper()} vs QUACKERS \n {amount} QuackCoins on the table for {roll} rounds !!!\n" + ' \n'
        response, result = qgames.dices(interaction.guild.id, roll, amount, name)
        response = intro + response

        if result == 0:
            amount *= -1
        elif result == 2:
            amount = 0

        qdb.add(interaction.guild.id, name, amount)
        if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
            qdb.add(interaction.guild.id, interaction.user.name, random.randint(0,qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value")))
        qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="GAME", amount=amount)
    else:
        response = "Not enough QuackCoins"

    await interaction.response.send_message(response)


@bot.slash_command(name="rps", description="Gamble QuackCoins against Quackers by playing Rock Paper Scissors ...", guild_ids= serv_list(list(set(qdb.get_server_list("rps")) & set(qdb.get_server_list("eco")) & set(qdb.get_server_list("game")))))
async def rps(
    interaction: Interaction,
    bet: int,
    element: int = SlashOption(
        name="picker",
        description="Pick something :",
        choices={"scissors": 0, "paper": 1, "rock": 2, "lizard": 3, "spock": 4},
    ),
):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    name = interaction.user.name

    if qdb.get_server_info(interaction.guild.id, "game_limit")==True and qdb.get_server_info(interaction.guild.id, "game_limit_value")>bet:
        bet = qdb.get_server_info(interaction.guild.id, "game_limit_value")

    if bet <= 0:
        bet = 1

    # CHECK MONEY
    money_check = qdb.qcheck(interaction.guild.id, name, bet)

    if money_check == 0:
        result, mult = qgames.rps(interaction.guild.id, element, bet, name)

        bet *= mult
        qdb.add(interaction.guild.id, name, bet)
        if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
            qdb.add(interaction.guild.id, interaction.user.name, random.randint(0,qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value")))
        qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="GAME", amount=bet)
    else:
        result = "Not enough QuackCoins available."
    await interaction.response.send_message(result)


@bot.slash_command(name="8ball", description="Quackers gives answers to any questions. [YES or NO questions]", guild_ids= serv_list(list(set(qdb.get_server_list("hball")) & set(qdb.get_server_list("eco")) & set(qdb.get_server_list("game")))))
async def eightball(interaction: Interaction, question: str):
    result = qgames.hball(interaction.user.name)
    message = f'> {interaction.user.name.capitalize()} asked : " *{question}* " \n {result}'
    if qdb.get_server_info(interaction.guild.id, "eco_pss_cmd")==True:
            qdb.add(interaction.guild.id, interaction.user.name, random.randint(0,qdb.get_server_info(interaction.guild.id, "eco_pss_cmd_value")))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)
    await interaction.response.send_message(message)

# BETTING SYSTEM
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
        id = qgames.bet_create(interaction.user.name, title, a, b)
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
        qdb.user_in_db(interaction.guild.id, interaction.user)

        if qgames.bet_status(self.id) == "open" and qgames.bet_has_betted(interaction.user.name, self.id) == 0:
            await interaction.response.send_modal(Betting(self.id, "A", interaction))
            self.value = True
        else:
            await interaction.response.send_message("THIS BET HAS BEEN CLOSED", ephemeral=True)

    @nextcord.ui.button(label="BET : B", style=nextcord.ButtonStyle.blurple)
    async def betb(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        qdb.user_in_db(interaction.guild.id, interaction.user)

        if qgames.bet_status(self.id) == "open" and qgames.bet_has_betted(interaction.user.name, self.id) == 0:
            await interaction.response.send_modal(Betting(self.id, "B", interaction))
            self.value = True
        else:
            await interaction.response.send_message("THIS BET HAS BEEN CLOSED", ephemeral=True)

class Betting(nextcord.ui.Modal):
    def __init__(self, id, option, interaction):
        super().__init__(
            title="BETTING",
            timeout=None,
        )
        self.id = id
        self.option = option

        self.amount = nextcord.ui.TextInput(
            label="AMOUNT",
            placeholder=str(int(qdb.get_server_info(interaction.guild.id, "bet_limit_value")*0.5)) if qdb.get_server_info(interaction.guild.id, "bet_limit")==True else "100",
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
            if qdb.get_server_info(interaction.guild.id, "bet_limit")==True and amount > qdb.get_server_info(interaction.guild.id, "bet_limit_value"):
                amount = qdb.get_server_info(interaction.guild.id, "bet_limit_value")
            if qdb.qcheck(interaction.guild.id, interaction.user.name, amount) == 0:
                qgames.bet_join(self.id, interaction.user.name, amount, self.option)
                qdb.add(interaction.guild.id, interaction.user.name, (amount * -1))
                await interaction.send(f"Confirming Joining Bet : {self.option}, with : {amount} QuackCoins", ephemeral=True)
            else:
                await interaction.send(f'{interaction.user.mention} do not have enough QuackCoins', ephemeral=True)

@bot.slash_command(name="bet-create", description="Create a BET", guild_ids= serv_list(list(set(qdb.get_server_list("bet")) & set(qdb.get_server_list("eco")) & set(qdb.get_server_list("game")))))
async def bet_create(interaction: nextcord.Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    if qgames.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_modal(BetCreation())
        qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="COMMAND", amount=1)
    else:
        await interaction.response.send_message('You already have a Bet going on. || send results of your bet before creating another one "/bet-result"', ephemeral=True)


@bot.slash_command(name="bet-close", description="Close a BET, users won't be able to bet on it.", guild_ids= serv_list(list(set(qdb.get_server_list("bet")) & set(qdb.get_server_list("eco")) & set(qdb.get_server_list("game")))))
async def bet_close(interaction: nextcord.Interaction):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    if qgames.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_message('You do not have any bet going on', ephemeral=True)
    else:
        totala, totalb, totalbetter, totalbettera, totalbetterb, highest = qgames.bet_close(interaction.user.name)
        # GET INFO FROM THE BET
        await interaction.response.send_message('Status Updated', ephemeral=True)
        mess = "BET CLOSED !!! \n \n"
        mess += f"{totalbetter} Users entered the bet. \n"
        mess += f"A : **{totala}** QuackCoins by {totalbettera} user(s) \n"
        mess += f"B : **{totalb}** QuackCoins by {totalbetterb} user(s) \n"
        mess += f"The highest bet was by : {highest}"
        await interaction.send(mess)


@bot.slash_command(name="bet-result", description="Sends the money", guild_ids= serv_list(list(set(qdb.get_server_list("bet")) & set(qdb.get_server_list("eco")) & set(qdb.get_server_list("game")))))
async def bet_result(
    interaction: Interaction,
    option: int = SlashOption(
        name="winner",
        description="Pick the winning option :",
        choices={"A": 0, "B": 1},
    ),
):
    qdb.user_in_db(interaction.guild.id, interaction.user)

    if qgames.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_message('You do not have any bet going on', ephemeral=True)
    else:
        option = "A" if option == 0 else "B"
        qgames.bet_result(interaction.guild.id, interaction.user.name, option)
        await interaction.response.send_message('MONEY SENT !!!')

@bot.slash_command(name="roll", description="Roll a dice", guild_ids=serv_list(list(set(qdb.get_server_list("eco")) & set(qdb.get_server_list("roll")))))
async def roll(
        interaction: Interaction,
    sides: Optional[int] = SlashOption(
        required=False, 
        description="Number of sides on the dice (e.g., 6 for a d6)"
    ),
    number: Optional[int] = SlashOption(
        required=False, 
        description="Number of dice to roll (default is 1)"
    )
):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    rolllist = []
    emojili = [" ✨ ", " 💩 "]

    if sides is None:
        sides = 20
    elif sides <= 0:
        sides = 20

    if number is None:
        number = 1
    elif number <= 0:
        number = 1

    for i in range(number):
        rolllist.append(random.randint(1, sides))

    sumroll = sum(rolllist)
    
    if sumroll == sides*number:
        emoji = emojili[0]
    elif sumroll == number:
        emoji = emojili[1]
    else:
        emoji = ""

    message = f"🎲 {interaction.user.name} rolled a {sides}-sided dice {number} times: {rolllist}"
    message += f"\n{emoji}Total: **{sumroll}**{emoji}"
    qdb.add(interaction.guild.id, interaction.user.name, random.randint(0, 5))
    qdb.add_stat(guild=interaction.guild.id, user=interaction.user.name, type="GAME", amount=1)
    await interaction.response.send_message(message)


# ADMIN
def is_admin(interaction: Interaction) -> bool:
    if interaction.user.id == interaction.guild.owner_id:
        return True
    if interaction.user.guild_permissions.administrator:
        return True

@bot.slash_command(name="admin-add", description="[ADMIN] add QuackCoins to a User", guild_ids= serv_list(qdb.get_server_list("eco")))
async def admin_add(interaction: Interaction, amount: int, user: nextcord.Member):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    qdb.user_in_db(interaction.guild.id, user)

    if not is_admin(interaction):
        await interaction.response.send_message("You do not have permission to use this command.")
        return

    name = interaction.user.name
    user_name = user.name

    qdb.add(interaction.guild.id, user_name, amount)
    result = qlogs.admin(f"[ADMIN : {name}] ADDED {amount} <:quackCoin:1124255606782578698> to {user_name.upper()}")

    await interaction.response.send_message(result)


@bot.slash_command(name="admin-remove", description="[ADMIN] remove QuackCoins from a User", guild_ids= serv_list(qdb.get_server_list("eco")))
async def admin_remove(interaction: Interaction, amount: int, user: nextcord.Member):
    qdb.user_in_db(interaction.guild.id, interaction.user)
    qdb.user_in_db(interaction.guild.id, user)

    if not is_admin(interaction):
        await interaction.response.send_message("You do not have permission to use this command.")
        return

    name = interaction.user.name
    user_name = user.name

    qdb.add(interaction.guild.id, user_name, (amount * -1))
    result = qlogs.admin(f"[ADMIN : {name}] REMOVED {amount} <:quackCoin:1124255606782578698> from {user_name.upper()}")

    await interaction.response.send_message(result)


@bot.slash_command(name="admin-logs", description="[ADMIN] Retrieve last 5 lines from LOGS", guild_ids= serv_list(testid))
async def admin_logs(interaction: Interaction):
    if not is_admin(interaction):
        await interaction.response.send_message("You do not have permission to use this command.")
        return
    
    try:
        # Read the last 5 lines from qlogs.log
        with open(LOGFILE, "r") as log_file:
            lines = log_file.readlines()[-5:]  # Get the last 5 lines

        # Send the lines as a code block
        formatted_lines = "".join(lines)
        await interaction.response.send_message(f"```\n{formatted_lines}\n```")
    except FileNotFoundError:
        await interaction.response.send_message("Error: qlogs.log file not found.")


@bot.slash_command(name="admin-scan", description="[ADMIN] scans the server and retrieves details about channels and roles.") #NO GUILD SPECIFIED SO ANY SERVER CAN BE ADDED
async def admin_scan(interaction: Interaction):
    guild = interaction.guild  # Get the guild (server) where the command was invoked

    if not guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return

    if not is_admin(interaction):
        await interaction.response.send_message("You do not have permission to use this command.")
        return

    # Get the server ID and name
    server_id = guild.id
    server_name = guild.name

    qdb.add_server(server_id, server_name)

    # Construct a response message
    response_message = (
        f"**Server Name**: {server_name}\n"
        f"**Server ID**: {server_id}\n"
        f"**Voice Channels**: {len(guild.voice_channels)}\n"
        f"**Text Channels**: {len(guild.text_channels)}\n"
        f"**Roles**: {len(guild.roles)}\n"
        f"**Members**: {guild.member_count}\n"
        f"**Owner**: {guild.owner.name}\n"
        f"**Created At**: {guild.created_at}\n"
        f"**Emoji Count**: {len(guild.emojis)}\n"
        f"\n \n"
        f"To SETUP the QUACKERS go to :: [QUACKERS](<https://quackersbot.com/setup>)\n"
        f"To Locally Setup the BOT :: [GITHUB](<https://github.com/FrenchFive/quackers/wiki>)\n"
    )

    # Send the initial message with server details
    await interaction.response.send_message(response_message)


#TASKS
@tasks.loop(hours=24)
async def daily_update():

    for server in serverid:
        if qdb.get_server_info(server, "bnk_itrs")==True and qdb.get_server_info(server, "bnk")==True:
            interest_rate = (qdb.get_server_info(server, "bnk_itrs_value")/(datetime(datetime.now().year, datetime.now().month % 12 + 1, 1) - timedelta(days=1)).day) 
            qlogs.info(f"Updating BANK : {interest_rate} % :: {server}")
            qdb.bank_update(server, interest_rate)

            channel = bot.get_channel(qdb.get_server_info(server, "dbg_ch_id"))
            if channel and qdb.get_server_info(server, "dbg_ch")==True:
                await channel.send("BANK HAS BEEN UPDATED")
    
    qdb.backup_db()

@daily_update.before_loop
async def before_daily_update():
    await bot.wait_until_ready()  # Wait until the bot is ready
    qlogs.info("Waiting for BANK")

    # Calculate the time until the next midnight
    now = datetime.now()
    next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_time = (next_midnight - now).total_seconds()

    qlogs.info(f"Waiting for {wait_time} seconds until the next midnight...")
    await asyncio.sleep(wait_time)  # Wait until the next midnight

@tasks.loop(hours=7*24)
async def weekly_update():
    qlogs.info("WEEKLY UPDATE")

    for server in serverid:

        type_totals, type_min_max, unique_names_count, interval_totals, type_most_entries = qdb.get_stats(server)

        path = qdraw.stat(interval_totals)
        imgfile = nextcord.File(path)

        message = ["**📊 Server Activity Statistics**"]

        # Add total messages and unique users
        message.append(f"\n**Total Unique Users:** `{unique_names_count}`")

        # TOTALS
        if "ARR" in dict(type_totals):
            message.append(f"\n**New Members This Week:** `{dict(type_totals)['ARR'] - dict(type_totals)['DEP']}`")
        if "MESS" in dict(type_totals):
            message.append(f"\n**Message Quantity This Week:** `{dict(type_totals)['MESS']}`")
        if "VC_CON" in dict(type_totals):
            message.append(f"\n**Voice Connection Quantity This Week:** `{dict(type_totals)['VC_CON']}`")
        if "COMMAND" in dict(type_totals) or "GAME" in dict(type_totals):
            try:
                cmd = dict(type_totals)['COMMAND']
            except:
                cmd = 0
            try:
                game = dict(type_totals)['GAME']
            except:
                game = 0
            message.append(f"\n**Commands Quantity This Week:** `{cmd + game}`")

        # Add type totals
        message.append("\n\n**Activity Summary:**")
        for activity, count in type_totals:
            message.append(f"- **{activity}:** `{count}` entries")

        # Add detailed stats for each type
        message.append("\n\n**Detailed Statistics by Type:**")
        for activity, min_amount, max_amount, min_author, max_author in type_min_max:
            if activity == "MESS":
                message.append(
                    f"- **Messages:**\n   - Longest message by `{max_author}`: `{max_amount}` characters"
                )
            elif activity == "VC_HOURS":
                message.append(
                    f"- **Voice Channel Time:**\n   - Longest session by `{max_author}`: `{max_amount}` hours"
                )
            elif activity == "GAME":
                message.append(
                    f"- **Game Interactions:**\n   - Biggest gamble by `{max_author}`: `{max_amount}` <:quackCoins:1124255606782578698>"
                )

        # Add most active users by type
        message.append("\n\n**Most Active Users by Type:**")
        if "MESS" in type_most_entries:
            message.append(f"- **Most Messages Sent:** `{type_most_entries['MESS']}`")
        if "VC_CON" in type_most_entries:
            message.append(f"- **Most Voice Channel Connections:** `{type_most_entries['VC_CON']}`")
        if "GAME" in type_most_entries:
            message.append(f"- **Most Games Played:** `{type_most_entries['GAME']}`")
        if "COMMAND" in type_most_entries:
            message.append(f"- **Most Commands used:** `{type_most_entries['COMMAND']}`")  

        # Combine all parts into a single string
        mess = "\n".join(message)
        mess = mess[:1000] #Cutting too long message

        channel = bot.get_channel(qdb.get_server_info(server, "admin_ch_id"))
        if channel:
            await channel.send(mess, file=imgfile)
            
        qdb.clear_stats(guild=server) #CLEAR STATS


@weekly_update.before_loop
async def before_weekly_update():
    await bot.wait_until_ready()

    # Calculate the time until the next sunday at midnight
    now = datetime.now()
    next_sunday = (now + timedelta(days=(7 - now.weekday()))).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_time = (next_sunday - now).total_seconds()

    qlogs.info(f"Waiting for {wait_time} seconds until the next Sunday...")
    await asyncio.sleep(wait_time)

# EVENTS
#QUACKER IS READY 
@bot.event
async def on_ready():
    qlogs.info("QUACKERS IS ONLINE")

    if not daily_update.is_running():
        daily_update.start()
    if not weekly_update.is_running():
        weekly_update.start()

    for guild in bot.guilds:
        qdb.add_server(guild.id, guild.name)

@bot.event
async def on_guild_join(guild):
    qdb.add_server(guild.id, guild.name)
    qlogs.info(f"QUACKERS has joined {guild.name}")

@bot.event
async def on_message(ctx):
    if ctx.guild is None or ctx.author == bot.user:
        return

    qdb.user_in_db(ctx.guild.id, ctx.author)

    qdb.add_mess(ctx.guild.id, ctx.author.name)
    qdb.add_stat(guild=ctx.guild.id, user=ctx.author.name, type="MESS", amount=len(ctx.content))
    if qdb.get_server_info(ctx.guild.id, "eco_pss_msg")==True:
        qdb.add(ctx.guild.id, ctx.author.name, qdb.get_server_info(ctx.guild.id, "eco_pss_msg_value"))

    #COIFFEUR
    pattern = re.compile(r"(?:^|\s)[qQ]+[uU]+[oO]+[iI]+[!? ]*$")
    feurlist = ["...feur","FEUR","FEUR !!!","feur","FEUUUUUR","coubeh!","kwak"]
    if bool(pattern.search(ctx.content)) == True and random.randint(0, 100) < 30:
        await ctx.channel.send(random.choice(feurlist))

    if qdb.get_server_info(ctx.guild.id, "ai_chat") and bot.user.mentioned_in(ctx)==True:
        qdb.add_quackers(ctx.guild.id, ctx.author.name)
        qdb.add(ctx.guild.id, ctx.author.name, 10)
        qlogs.info(f'// RESPONDING TO : {ctx.author.name}')

        message = unidecode(qopenai.generate_response(ctx.content, ctx.author.name))

        chunk = 1800
        if len(message) < chunk:
            await ctx.channel.send(message)
        else:
            li_tosend = [message[i:i + chunk] for i in range(0, len(message), chunk)]
            for mess in li_tosend:
                await ctx.channel.send(mess)
        
        qopenai.update_memory_summary()
    else:
        await bot.process_commands(ctx)
        return

def vc_connection(guild, member):
    # User connected to a voice channel
    qdb.voiceactive(guild.id, member.name)
    qdb.add(guild.id, member.name, qdb.get_server_info(guild.id, "eco_pss_ch_value"))
    qlogs.info(f"{member.name} is connected to a Voice Channel :: {guild.name}")

    qdb.add_stat(guild=guild.id, user=member.name, type="VC_CON", amount=1)

def vc_disconnect(guild, member):
    # User disconnected from a voice channel
    hours = qdb.voicestalled(guild.id, member.name)
    qlogs.info(f"{member.name} is disconnected")

    qdb.add_stat(guild=guild.id, user=member.name, type="VC_HOUR", amount=hours)

@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    qdb.user_in_db(guild.id, member)

    if before.channel is None and after.channel is not None:
        vc_connection(guild, member)
    
    if after.channel is not None and before.channel is not None and before.channel.id == qdb.get_server_info(guild.id, "eco_pss_ch_afk_id") and qdb.get_server_info(guild.id, "eco_pss_ch_afk")==True:
        vc_connection(guild, member)

    if before.channel is not None and after.channel.id == qdb.get_server_info(guild.id, "eco_pss_ch_afk_id") and qdb.get_server_info(guild.id, "eco_pss_ch_afk")==True:
        vc_disconnect(guild, member)

    if before.channel is not None and after.channel is None:
        if before.channel.id == qdb.get_server_info(guild.id, "eco_pss_ch_afk_id") and qdb.get_server_info(guild.id, "eco_pss_ch_afk")==True:
            pass
        else:
            vc_disconnect(guild, member)

#WELCOME and GOODBYE
@bot.event
async def on_member_join(member):
    guild = member.guild

    qlogs.info(f"{member.name} has joined the server :: {guild.name}")
    
    qdb.user_in_db(guild.id, member)
    
    if qdb.get_server_info(guild.id, "wlc")==True:
        if qdb.get_server_info(guild.id, "wlc_msg")==True:
            welcomemsg = qdb.get_server_info(guild.id, "wlc_msg_content").replace("{name}", member.mention)
        else:
            with open(os.path.join(TXT_PATH, "welcome.txt"), "r") as file:
                welcome_message = file.readlines()
            welcomemsg = random.choice(welcome_message).replace("{name}", member.mention)

        channel = bot.get_channel(qdb.get_server_info(guild.id, "wlc_ch_id"))
        if channel:
            message = await channel.send(welcomemsg)
            if qdb.get_server_info(guild.id, "wlc_rct")==True:
                emojis = ["\U0001F44C", "\U0001F4AF", "\U0001F389", "\U0001F38A"]
                if qdb.get_server_info(guild.id, "wlc_rct_cstm")==True:
                    server_emojis = guild.emojis
                    emojis.extend([str(e) for e in server_emojis])
                await message.add_reaction(random.choice(emojis))
    
    #ROLE ASSIGNEMENT
    if qdb.get_server_info(guild.id, "prst")==True:
        role_new = qdb.get_server_info(guild.id, "prst_role")
        role = guild.get_role(role_new)

        if role:
            await member.add_roles(role, reason="Assigned role upon joining the server.")
            print(f"Assigned role '{role.name}' to {member.name}.")
        else:
            print(f"Role '{role.name}' not found in the server.")
    
    
    # Send a private message to the user
    if qdb.get_server_info(guild.id, "dm")==True:
        message_welcome = qdb.get_server_info(guild.id, "dm_msg_content").replace("{name}", member.name)
        if len(message_welcome) <= 1:
            with open(os.path.join(TXT_PATH, "welcome_private.txt"), "r", encoding='utf-8') as file:
                message_welcome = file.read()
        try:
            await member.send(message_welcome)
            qlogs.info(f"- Sent a welcome message to {member.name}")
        except Exception as e:
            qlogs.error(f"Failed to send a welcome message to {member.name}: {e}")
    
    qdb.add_stat(guild=guild.id, user=member.name, type="ARR", amount=1)


@bot.event
async def on_member_remove(member):
    guild = member.guild
    qlogs.info(f"{member.name} has left the server :: {guild.name}")

    if qdb.get_server_info(guild.id, "gdb")==True:
        channel = bot.get_channel(qdb.get_server_info(guild.id, "gdb_ch_id"))
        if qdb.get_server_info(guild.id, "gdb_msg")==True:
            message = qdb.get_server_info(guild.id, "gdb_msg_content").replace("{name}", member.name)
        else:
            with open(os.path.join(TXT_PATH, "goodbye.txt"), "r") as file:
                goodbye_message = file.readlines()
            message = random.choice(goodbye_message).replace("{name}", member.name)
        if channel:
            await channel.send(message)
    
    qdb.add_stat(guild=guild.id, user=member.name, type="DEP", amount=1)


if __name__ == "__main__":
    if KEY_DISCORD == None:
        print("Error: There is currently no 'KEY_DISCORD' environment variable. Please create a .env with the required values.")
        exit(1)
    bot.run(KEY_DISCORD)
    exit(0)
