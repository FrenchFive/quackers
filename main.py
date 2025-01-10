# -*- coding: utf-8 -*-
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from typing import Optional

from unidecode import unidecode

import openai
from datetime import datetime

import qdatabase as qdb
import qgames
import qdraw
import qopenai
import qlogs

import os
import random

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

# Server IDs
serverid = qdb.get_all_server_ids()
testid = [1159282148042350642]

#SERVER QUESTIONS
questions = [
    {"q": "Select an Admin Role", "type": "role", "format": "name"},
    {"q": "Select a Newbie Role", "type": "role", "format": "name"},
    {"q": "Select an AFK Voice Channel", "type": "audio", "format": "name"},
    {"q": "Select a General Channel", "type": "text", "format": "id"},
    {"q": "Select a Debugging Channel", "type": "text", "format": "id"},
    {"q": "Select a Welcome Channel", "type": "text", "format": "id"},
    {"q": "Select an Admin Info Channel", "type": "text", "format": "id"},
    
]

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
        if qdb.user_in_db(interaction.user.name) == 0:
            qdb.add_user(interaction.user.name)
        if qgames.bet_status(self.id) == "open" and qgames.bet_has_betted(interaction.user.name, self.id) == 0:
            await interaction.response.send_modal(Betting(self.id, "A"))
            self.value = True
        else:
            await interaction.response.send_message("THIS BET HAS BEEN CLOSED", ephemeral=True)

    @nextcord.ui.button(label="BET : B", style=nextcord.ButtonStyle.blurple)
    async def betb(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if qdb.user_in_db(interaction.user.name) == 0 and qgames.bet_has_betted(interaction.user.name, self.id) == 0:
            qdb.add_user(interaction.user.name)
        if qgames.bet_status(self.id) == "open":
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
                qgames.bet_join(self.id, interaction.user.name, amount, self.option)
                qdb.add(interaction.user.name, (amount * -1))
                await interaction.send(f"Confirming Joining Bet : {self.option}, with : {amount} QuackCoins", ephemeral=True)
            else:
                await interaction.send(f'{interaction.user.mention} do not have enough QuackCoins', ephemeral=True)

class PresentationModal(nextcord.ui.Modal):
    def __init__(self, target_channel, user, imgpath):
        super().__init__(
            title="PRESENTATIONS",
            timeout=None,
        )

        self.target_channel = target_channel  # Save the target channel ID
        self.user = user
        self.img = imgpath

        # Questions
        self.pronouns = nextcord.ui.TextInput(
            label="Pronouns",
            placeholder="He/Him, She/Her, They/Them, ...",
            required=True,
        )
        self.add_item(self.pronouns)

        self.favorite_color = nextcord.ui.TextInput(
            label="Favorite Color",
            placeholder="Purple...",
            required=False,
        )
        self.add_item(self.favorite_color)

        self.introduced_by = nextcord.ui.TextInput(
            label="Who introduced you to the server?",
            placeholder="Mention the user @username",
            required=True,
        )
        self.add_item(self.introduced_by)

        self.favorite_animal = nextcord.ui.TextInput(
            label="Favorite Animal",
            placeholder="Cats, Dogs, Land Sharks, Ducks, ...",
            required=True,
        )
        self.add_item(self.favorite_animal)

        self.fun_fact = nextcord.ui.TextInput(
            label="Fun Fact About You",
            placeholder="Share something interesting about yourself!",
            required=False,
        )
        self.add_item(self.fun_fact)

    async def callback(self, interaction: nextcord.Interaction):
        # Dynamically generate a summary of the user's responses
        responses = [f"**Submitted By**: {self.user}"]

        if self.pronouns.value:
            responses.append(f"**Pronouns**: {self.pronouns.value}")
        if self.favorite_color.value:
            responses.append(f"**Favorite Color**: {self.favorite_color.value}")
        if self.introduced_by.value:
            responses.append(f"**Introduced By**: {self.introduced_by.value}")
        if self.favorite_animal.value:
            responses.append(f"**Favorite Animal**: {self.favorite_animal.value}")
        if self.fun_fact.value:
            responses.append(f"**Fun Fact**: {self.fun_fact.value}")
         
        # Send a thank-you message to the user
        await interaction.response.send_message(
            "Thank you for introducing yourself! Your responses have been recorded.",
            ephemeral=True,
        )

        embed = nextcord.Embed(
            title=f"🎉 Welcome {self.user} to the Server! 🎉",
            description="Here's their introduction!",
            color=nextcord.Color.random(),
        )

        # Send the combined message to the target channel
        if responses:
            response_message = "\n".join(responses)
            embed.add_field(name="Presentation", value=response_message, inline=False)
            target_channel = interaction.guild.get_channel(self.target_channel)
            if target_channel:
                with open(self.img, 'rb') as img_file:
                    file = nextcord.File(img_file, filename="thumbnail.png")
                    embed.set_thumbnail(url=f"attachment://thumbnail.png")
                    await target_channel.send(embed=embed, file=file)
            else:
                print(f"Error: Channel {self.target_channel} not found.")

class DynamicQuestionDropdown(nextcord.ui.Select):
    def __init__(self, question, items):
        options = [
            nextcord.SelectOption(label=name, value=str(id_)) for id_, name in items.items()
        ]
        super().__init__(
            placeholder=question["q"],
            min_values=1,
            max_values=1,
            options=options,
        )
        self.question = question
        self.selected_value = None

    async def callback(self, interaction: Interaction):
        # Store the selected value
        self.selected_value = self.values[0]
        await interaction.response.defer()  # Acknowledge the interaction



class DynamicQuestionDropdown(nextcord.ui.Select):
    def __init__(self, question, items):
        # Truncate items if there are too many
        max_option= 24
        if len(items) > max_option:
            truncated_items = dict(list(items.items())[:max_option])
            truncated_items["..."] = "Too many items, truncated"
        else:
            truncated_items = items

        options = [
            nextcord.SelectOption(label=name, value=str(id_)) for id_, name in truncated_items.items()
        ]
        super().__init__(
            placeholder=question["q"],
            min_values=1,
            max_values=1,
            options=options,
        )
        self.question = question
        self.selected_value = None

    async def callback(self, interaction: Interaction):
        # Store the selected value
        self.selected_value = self.values[0]
        await interaction.response.defer()  # Acknowledge the interaction


class DynamicQuestionView(nextcord.ui.View):
    def __init__(self, questions, guild, current_index=0, answers=None):
        super().__init__()
        self.questions = questions
        self.guild = guild
        self.current_index = current_index
        self.answers = answers or {}

        # Add the dropdown for the current question
        question = questions[current_index]
        items = self.get_items(question)
        if items:
            dropdown = DynamicQuestionDropdown(question, items)
            self.add_item(dropdown)

        # Add the "Next" button
        next_button = nextcord.ui.Button(label="Next", style=nextcord.ButtonStyle.primary)
        next_button.callback = self.next_button_callback  # Attach the callback
        self.add_item(next_button)

    def get_items(self, question):
        if question["type"] == "audio":
            items = {channel.id: channel.name for channel in self.guild.voice_channels}
        elif question["type"] == "text":
            items = {channel.id: channel.name for channel in self.guild.text_channels}
        elif question["type"] == "role":
            items = {role.id: role.name for role in self.guild.roles}
        else:
            items = {}

        # Truncate items if necessary
        max_option = 24
        if len(items) > max_option:
            truncated_items = dict(list(items.items())[:max_option])
            truncated_items["..."] = "Too many items, truncated"
            return truncated_items
        return items

    async def next_button_callback(self, interaction: Interaction):
        # Collect the answer from the dropdown
        for child in self.children:
            if isinstance(child, DynamicQuestionDropdown) and child.selected_value:
                # Save based on the "format"
                question = self.questions[self.current_index]
                if question["format"] == "name":
                    self.answers[question["q"]] = self.get_items(question).get(
                        int(child.selected_value), "Unknown"
                    )
                elif question["format"] == "id":
                    self.answers[question["q"]] = child.selected_value

        # Move to the next question
        if self.current_index + 1 < len(self.questions):
            next_view = DynamicQuestionView(
                questions=self.questions,
                guild=self.guild,
                current_index=self.current_index + 1,
                answers=self.answers,
            )
            await interaction.response.edit_message(
                content=f"**{self.questions[self.current_index + 1]['q']}**",
                view=next_view,
            )
        else:
            # All questions answered
            answer_text = "\n".join(
                f"**{question}**: {value}" for question, value in self.answers.items()
            )
            # Explicitly map answers to database fields
            qdb.add_or_update_server(
                server_id=self.guild.id,
                server_name=self.guild.name,
                vc_afk=self.answers.get("Select an AFK Voice Channel", None),
                channel_welcome_id=self.answers.get("Select a Welcome Channel", None),
                channel_info_id=self.answers.get("Select an Admin Info Channel", None),
                channel_test_id=self.answers.get("Select a Debugging Channel", None),
                channel_general_id=self.answers.get("Select a General Channel", None),
                role_newbie_name=self.answers.get("Select a Newbie Role", None),
                role_admin_name=self.answers.get("Select an Admin Role", None),
            )

            await interaction.response.edit_message(
                content=f"Here are your selections:\n\n{answer_text}",
                view=None,  # Remove the view
            )

#QUACKER IS READY 
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


@bot.slash_command(name="presentation", description="Introduce yourself to the server!", guild_ids=serverid)
async def introduce(interaction: nextcord.Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)
    
    guild = interaction.guild
    role_newbies = qdb.get_role_newbie(guild.id)
    role = next((role for role in guild.roles if role.name == role_newbies), None)
    if role is None:
        await interaction.response.send_message(
            "Required role not found in the server.",
            ephemeral=True,
        )
        return

    user_roles = interaction.user.roles
    has_required_role = any(role.name == role_newbies for role in user_roles)
    if not has_required_role:
        await interaction.response.send_message(
            "You do not have the required role to use this command.",
            ephemeral=True,
        )
        return

    url = interaction.user.display_avatar.url
    imgpath = qdraw.avatar_download(url)

    channel_welcome = qdb.get_ch_welcome(guild.id)
    await interaction.response.send_modal(PresentationModal(target_channel=channel_welcome, user=interaction.user.name, imgpath=imgpath))

    await interaction.user.remove_roles(role, reason="Role removed after presentation completion.")
    print(f"Role '{role_newbies}' removed from {interaction.user.name}.")

# qgames
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
        response, result = qgames.dices(roll, amount, name)
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
        result, mult = qgames.rps(element, bet, name)

        bet *= mult
        qdb.add(name, bet)
        qdb.add(interaction.user.name, random.randint(0, 5))
    else:
        result = "Not enough QuackCoins available."
    await interaction.response.send_message(result)


@bot.slash_command(name="8ball", description="Quackers gives answers to any questions. [YES or NO questions]", guild_ids=serverid)
async def eightball(interaction: Interaction, question: str):
    result = qgames.hball(interaction.user.name)
    message = f'> {interaction.user.name.capitalize()} asked : " *{question}* " \n {result}'
    qdb.add(interaction.user.name, random.randint(0, 5))
    await interaction.response.send_message(message)


# BETTING SYSTEM
@bot.slash_command(name="bet-create", description="Create a BET", guild_ids=serverid)
async def bet_create(interaction: nextcord.Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

    if qgames.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_modal(BetCreation())
    else:
        await interaction.response.send_message('You already have a Bet going on. || send results of your bet before creating another one "/bet-result"', ephemeral=True)


@bot.slash_command(name="bet-close", description="Close a BET, users won't be able to bet on it.", guild_ids=serverid)
async def bet_close(interaction: nextcord.Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)

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

    if qgames.bet_has_a_bet_going_on(interaction.user.name) == 0:
        await interaction.response.send_message('You do not have any bet going on', ephemeral=True)
    else:
        option = "A" if option == 0 else "B"
        qgames.bet_result(interaction.user.name, option)
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

@bot.slash_command(name="admin-scan", description="Scans the server and retrieves details about channels and roles.") #NO GUILD SPECIFIED SO ANY SERVER CAN BE ADDED
async def admin_scan(interaction: Interaction):
    guild = interaction.guild  # Get the guild (server) where the command was invoked

    if not guild:
        await interaction.response.send_message("This command can only be used in a server.")
        return

    # Get the server ID and name
    server_id = guild.id
    server_name = guild.name

    # Construct a response message
    response_message = (
        f"**Server Name**: {server_name}\n"
        f"**Server ID**: {server_id}\n"
        f"**Voice Channels**: {len(guild.voice_channels)}\n"
        f"**Text Channels**: {len(guild.text_channels)}\n"
        f"**Roles**: {len(guild.roles)}\n"
    )

    # Send the initial message with server details
    await interaction.response.send_message(response_message)

    # Start with the first question
    question = questions[0]
    view = DynamicQuestionView(questions, guild)
    await interaction.followup.send(
        f"**{question['q']}**",
        view=view,
    )


# EVENTS
@bot.event
async def on_message(ctx):
    if ctx.guild is None or ctx.author == bot.user:
        return

    if qdb.user_in_db(ctx.author.name) == 0:
        qdb.add_user(ctx.author.name)

    qdb.add_mess(ctx.author.name)

    #COIFFEUR
    pattern = re.compile(r"(?:^|\s)[qQ]+[uU]+[oO]+[iI]+[!? ]*$")
    feurlist = ["...feur","FEUR","FEUR !!!","feur","FEUUUUUR","coubeh!","kwak"]
    if bool(pattern.search(ctx.content)) == True:
        await ctx.channel.send(random.choice(feurlist))

    if not bot.user.mentioned_in(ctx):
        await bot.process_commands(ctx)
        return

    qdb.add_quackers(ctx.author.name)
    qlogs.info(f'// RESPONDING TO : {ctx.author.name}')

    message = unidecode(qopenai.generate_response(ctx.content, ctx.author.name))

    chunk = 1800
    if len(message) < chunk:
        await ctx.channel.send(message)
    else:
        li_tosend = [message[i:i + chunk] for i in range(0, len(message), chunk)]
        for mess in li_tosend:
            await ctx.channel.send(mess)


@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild

    if before.channel is None and after.channel is not None:
        # User connected to a voice channel
        if qdb.user_in_db(member.name) == 0:
            qdb.add_user(member.name)

        qdb.voiceactive(member.name)
        qdb.add(member.name, 15)
        qlogs.info(f"{member.name} is connected to a Voice Channel")

    if before.channel is None and after.channel.name == qdb.get_vc_afk(guild.id):
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

#WELCOME and GOODBYE
@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined the server")
    qlogs.info(f"{member.name} has joined the server")
    
    if qdb.user_in_db(member.name) == 0:
        qdb.add_user(member.name)
    
    guild = member.guild

    channel = bot.get_channel(qdb.get_ch_welcome(guild.id))
    if channel:
        message = await channel.send(f"Welcome {member.mention} sur le serveur de la team QUACK!")
        emojis = ["\U0001F44C", "\U0001F4AF", "\U0001F389", "\U0001F38A"]
        await message.add_reaction(random.choice(emojis))
    
    role_newbies = qdb.get_role_newbie(guild.id)
    role = next((r for r in guild.roles if r.name == role_newbies), None)

    if role:
        try:
            await member.add_roles(role, reason="Assigned role upon joining the server.")
            print(f"Assigned role '{role_newbies}' to {member.name}.")
        except Exception as e:
            print(f"Failed to assign role '{role_newbies}' to {member.name}: {e}")
    else:
        print(f"Role '{role_newbies}' not found in the server.")


@bot.event
async def on_member_remove(member):
    print(f"{member.name} has left the server")
    qlogs.info(f"{member.name} has left the server")

    guild = member.guild

    channel = bot.get_channel(qdb.get_ch_info(guild.id))
    if channel:
        await channel.send(f"{member.name} a quitte le serveur de la team QUACK!")


bot.run(KEY_DISCORD)
