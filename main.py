# -*- coding: utf-8 -*-
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord import SlashOption
from typing import Optional

from unidecode import unidecode

from openai import OpenAI
from datetime import datetime

import qdatabase as qdb
import games
import qdraw

import os
import random

import qlogs

import time

scrpt_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = 'txt'
FOLDER_PATH = os.path.join(scrpt_dir, folder_name)

ENV = os.path.join(scrpt_dir, "secret.env")
env_file = open(ENV, 'r')
env_data = env_file.readlines()
KEY_OPENAI = env_data[0].replace('\n','')
KEY_DISCORD = env_data[1].replace('\n','')
env_file.close()

LOGFILE = os.path.join(scrpt_dir, "qlogs.log")

bot = commands.Bot(command_prefix='!', intents= nextcord.Intents.all())

counter = 0

#OPEN AI INITIALISATION
CLIENT = OpenAI(api_key=KEY_OPENAI)
thread = CLIENT.beta.threads.create()
bot_id = "asst_DDSMrYNpgfEulWI85Ccg882z"

#serveur IDs
serverid = [1159282148042350642, 945445171670171668]
testid = [1159282148042350642]
afkchannellist = ["afk"]

def context():
    global thread
    global bot_id
    global scrpt_dir

    #DELETE FILES
    assistant_files = CLIENT.beta.assistants.files.list(assistant_id=bot_id)
    try:
        for file in assistant_files:
            CLIENT.beta.assistants.files.delete(
                assistant_id = bot_id,
                file_id = file.id
            )
            CLIENT.files.delete(file_id=file.id)
    except:
        pass

    #EXPORT DATABASE TO .json
    qdb.export()

    #ADD FILES
    for fi in os.listdir(FOLDER_PATH):
        filtmp = os.path.join(scrpt_dir, 'txt', fi)
        if os.path.getsize(filtmp) > 100:
            file_data = CLIENT.files.create(
                file=open(filtmp , "rb"),
                purpose="assistants"
            )
            CLIENT.beta.assistants.files.create(
                assistant_id = bot_id,
                file_id = file_data.id
            )
    
    print('-- ALL FILES PROCESSED')

context()

# OPENAI REQUEST FUNCTION
def generate():
    client = CLIENT
    global thread
    global bot_id
    #INITIALIZATION 

    #RUN
    print('-- RUNNING')
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=bot_id
    )

    starttime = time.time()
    error = 0
    print('-- WAITING GEN')
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.completed_at:
            print("-- GENERATED")
            break
        elif (time.time() - starttime)>180:
            print("error")
            error = 1
            break
    
    if error == 0:
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
    else:
        response = "I am having difficulties => see w/ Five"

    return(response)

#MODAL DISCORD
class BetCreation(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            title = "BET CREATION",
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
        if self.optionone.value == '':
            a = "YES"
        else:
            a = self.optionone.value
        if self.optiontwo.value == '':
            b = "NO"
        else:
            b = self.optiontwo.value
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
            title = "BETTING",
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
        except:
            amount = 0
            await interaction.send('Amount must be a number', ephemeral=True)
        
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


#COMMANDS
@bot.slash_command(name="daily", description="Receive daily QuackCoins.", guild_ids=serverid)
async def daily(interaction: Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)
    
    result = qdb.daily(interaction.user.name)
    qdb.add(interaction.user.name, 5)
    
    await interaction.response.send_message(result)

@bot.slash_command(name="send", description="Send QuackCoins to someone.", guild_ids=serverid)
async def send(interaction: Interaction, amount:int, user:nextcord.Member):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)
    
    if qdb.user_in_db(user.name) == 0:
        qdb.add_user(user.name)
    
    result = qdb.send(interaction.user.name, user.name, amount)
    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(result)

@bot.slash_command(name="coins", description="Gives you your QuackCoins balance.", guild_ids=serverid)
async def coins(interaction: Interaction, user:Optional[nextcord.Member]=SlashOption(required=False)):
    if user is None:
        name = interaction.user.name
    else:
        name = user.name
        if qdb.user_in_db(interaction.user.name) == 0:
            qdb.add_user(interaction.user.name)

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)
    
    result = qdb.coins(name)
    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(result)

@bot.slash_command(name="info", description="Get an Image of your Quack Profile", guild_ids=testid)
async def info(interaction: Interaction, user:Optional[nextcord.Member]=SlashOption(required=False)):
    if user is None:
        name = interaction.user.name
        url = interaction.user.display_avatar
    else:
        name = user.name
        url = user.display_avatar
        if qdb.user_in_db(interaction.user.name) == 0:
            qdb.add_user(interaction.user.name)

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)
    
    result = qdb.info(name)
    qdb.add(interaction.user.name, 5)
 
    qdraw.info(name, url, result)

    await interaction.response.send_message(result)

@bot.slash_command(name="leaderboard", description="Display the Top.10 of the server.", guild_ids=serverid)
async def leaderboard(interaction: Interaction):
    if qdb.user_in_db(interaction.user.name) == 0:
        qdb.add_user(interaction.user.name)
    
    intro = "HERE IS A LEADERBOARD OF THE CURRENT STATE OF THE QUACK COINS // \n"
    results = qdb.leaderboard()
    result = '\n'.join(results)
    message = intro + result

    qdb.add(interaction.user.name, 5)

    await interaction.response.send_message(message)


#GAMES
@bot.slash_command(name="dices", description="Gamble QuackCoins against Quackers by throwing dices.", guild_ids=serverid)
async def dices(interaction: Interaction, bet: Optional[int]=SlashOption(required=False), roll:Optional[int]=SlashOption(required=False)):
    if bet is None:
        bet = 100
    if roll is None:
        roll = 3

    amount = bet
    name = interaction.user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)
    
    if amount > 100:
        amount = 100
    if amount <= 0:
        amount = 1
    
    if roll>10:
        roll = 10
    
    #CHECK MONEY
    money_check = qdb.qcheck(name, amount)

    if money_check == 0:
        intro = f"{name.upper()} vs QUACKERS \n {amount} QuackCoins on the table for {roll} rounds !!!\n" + ' \n'
        response, result = games.dices(roll, amount, name)
        response = intro + response

        if result == 0:
            amount *= -1
        elif result == 2:
            amount = 0
        else:
            pass

        qdb.add(name, amount)
        qdb.add(interaction.user.name, random.randint(0, 5))
    else:
        response = "Not enough QuackCoins"

    await interaction.response.send_message(response)

@bot.slash_command(name="rps", description="Gamble QuackCoins against Quackers by playing Rock Paper Scissors ...", guild_ids=serverid)
async def rps(
    interaction: Interaction,
    bet:int,
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

    #CHECK MONEY
    money_check = qdb.qcheck(name, bet)
    
    if money_check == 0:
        result, mult = games.rps(element, bet, name)

        bet *= mult
        qdb.add(name, bet)
        qdb.add(interaction.user.name, random.randint(0, 5))
    else:
        result = "Pas assez de QuackCoins disponibles."
    await interaction.response.send_message(result)

#BETTING SYSTEM
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
        #GET INFO FROM THE BET
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
        if option == 0:
            option = "A"
        else:
            option = "B"
        games.bet_result(interaction.user.name, option)
        await interaction.response.send_message('MONEY SENT !!!')

#ADMIN
@bot.slash_command(name="admin-add", description="[ADMIN] add QuackCoins to a User", guild_ids=serverid)
async def add(interaction: Interaction, amount:int, user:nextcord.Member):
    name = interaction.user.name
    user = user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    if qdb.user_in_db(user) == 0:
        qdb.add_user(user)
    
    qdb.add(user, amount)
    result = qlogs.admin(f"[ADMIN : {name}] ADDED {amount} <:quackCoin:1124255606782578698> to {user.upper()}")

    await interaction.response.send_message(result)

@bot.slash_command(name="admin-remove", description="[ADMIN] remove QuackCoins to a User", guild_ids=serverid)
async def add(interaction: Interaction, amount:int, user:nextcord.Member):
    name = interaction.user.name
    user = user.name

    if qdb.user_in_db(name) == 0:
        qdb.add_user(name)

    if qdb.user_in_db(user) == 0:
        qdb.add_user(user)
    
    qdb.add(user, (amount*-1))
    result = qlogs.admin(f"[ADMIN : {name}] REMOVED {amount} <:quackCoin:1124255606782578698> to {user.upper()}")

    await interaction.response.send_message(result)

@bot.slash_command(name="admin-logs", description="[ADMIN] Retrieve last 5 lines from LOGS", guild_ids=serverid)
async def logs(interaction: Interaction):
    try:
        # Read the last 10 lines from q.log
        with open(LOGFILE, "r") as log_file:
            lines = log_file.readlines()[-5:]  # Get the last 10 lines

        # Send the lines as a code block
        formatted_lines = "\n".join(lines)
        await interaction.response.send_message(f"```\n{formatted_lines}\n```")
    except FileNotFoundError:
        await interaction.response.send_message("Error: q.log file not found.")

#EVENTS
@bot.event
async def on_message(ctx):
    global counter
    global thread
    if  ctx.guild is None or ctx.author == bot.user:
        return
    
    if qdb.user_in_db(ctx.author.name) == 0:
        qdb.add_user(ctx.author.name)
    
    qdb.add_mess(ctx.author.name)

    if bot.user.mentioned_in(ctx)==False:
        await bot.process_commands(ctx)
        return

    qdb.add_quackers(ctx.author.name)
    counter += 1
    qlogs.info(f'{counter:02} // RESPONDING TO : {ctx.author.name}')

    CLIENT.beta.threads.messages.create(
            thread.id,
            role="assistant",
            content=f'RESPOND SHORTLY to the following Message sent by : {ctx.author.name}, at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, USING THE PROVIDED FILES',
    )

    CLIENT.beta.threads.messages.create(
            thread.id,
            role="user",
            content=ctx.content,
    )
    
    message = unidecode(generate())
    
    chunk = 1800
    if len(message)<chunk:
        await ctx.channel.send(message)
    else:
        li_tosend = [message[i:i + chunk] for i in range(0, len(message), chunk)]
        for mess in li_tosend:
            await ctx.channel.send(mess)
    
    if counter >= 10:
        counter = 0
        CLIENT.beta.threads.messages.create(
            thread.id,
            role="user",
            content="WRITE DOWN A LIST OF IMPORTANT INFORMATIONS FOR YOU TO REMEMBER, DIFFERENT FROM THE 2 FIRST ASSISTANT MESSAGES. YOU CAN REWRITE AND COMPLETE THE MEMORY LIST MESSAGE PROVIDED ABOVE.",
        )
        memory = generate()
        memory_file_name = 'memory.txt'
        memory_file_path = os.path.join(FOLDER_PATH, memory_file_name)
        with open(memory_file_path, 'w', encoding='utf-8') as f:
            f.write(memory)
        temp = 'MEMORY LIST :' + '\n' + memory
        memory = temp
        qlogs.info("/// RESETTING THREAD")
        thread = CLIENT.beta.threads.create()
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
    if before.channel is None and  after.channel in afkchannellist:
        #USER CONNECTED TO AFK
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