import random

import os
import sqlite3
from sqlite3 import Error
import time
from datetime import datetime, timedelta

import qlogs
import qdatabase as qdb

scrpt_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = 'db/qbet.db'
database_path = os.path.join(scrpt_dir, folder_name)

CONNECTION = sqlite3.connect(database_path)
CURSOR = CONNECTION.cursor()
CURSOR.execute(' CREATE TABLE IF NOT EXISTS "dashboard" ("id" INTEGER UNIQUE, "user" TEXT, "title" TEXT, "status" TEXT, "A" TEXT, "B" TEXT, "total_a" INT, "total_b" INT, PRIMARY KEY("id" AUTOINCREMENT))')
CONNECTION.commit()

def roll(num):
    dicelist = []
    for i in range(num):
        dicelist.append(random.randint(1,6))
    return(dicelist)

def dices(num, money, name):
    botroll = roll(num)
    userroll = roll(num)

    bottotal = sum(botroll)
    usertotal = sum(userroll)

    response = ""
    for i in range(num):
        response+= f'ROUND {i+1}\n'
        response+= f'{name.capitalize()} rolls a {userroll[i]}\n'
        response+= f'Quackers rolls a {botroll[i]}\n'
        response+= ' \n'
    
    if bottotal > usertotal:
        response+= f'\nQuackers WON // with {bottotal} over {usertotal}\n'
        response+= f'{money} <:quackCoin:1124255606782578698> removed from {name} balance.'
        end = 0
    elif usertotal > bottotal :
        response+= f'\n{name.capitalize()} WON // with {usertotal} over {bottotal}\n'
        response+= f'{money} <:quackCoin:1124255606782578698> added to {name} balance.'
        end = 1
    else :
        response+= f'\nEGALITE !!! // with {usertotal} over {bottotal}\n'
        end = 2
    
    return(response, end)

def rps(user, bet, name):
    play = ["scissors","paper","rock","lizard","spock"]
    emoji = ['✂️', '🧻', '🪨', '🦎', '🖖']
    bot = random.randint(0, len(play)-1)

    if user == bot:
        gameresult = 0
        text = "EGALITE"
    elif user+1 == bot or user-2 == bot or user+1 == bot+5 or user-2 == bot-5:
        gameresult = 1
        text = f'\n {name} a GAGNE !!! // {bet} <:quackCoin:1124255606782578698> gagnés'
    elif bot+1 == user or bot-2 == user or bot+1 == user+5 or bot-2 == user-5:
        gameresult = -1
        text = f'\n {name} a PERDU !!! // {bet} <:quackCoin:1124255606782578698> perdus'
    else:
        return('ERROR', 0)
    
    tosay = f'{name} a joué : {play[user]} - {emoji[user]} \n'
    tosay += f'Quackers a joué : {play[bot]} - {emoji[bot]} \n'
    tosay += text

    return(tosay, gameresult)

#BET  
def bet_create(name, title, a, b):
    CURSOR.execute('INSERT INTO dashboard (user, title, status, a, b, total_a, total_b) VALUES(?, ?, ?, ?, ?, ?, ?)', (name, title, "open", a, b, 0, 0))
    CONNECTION.commit()
    inserted_id = CURSOR.lastrowid
    qlogs.info(f'--BET-DB // ADDED BET : {title} by {name}')
    CURSOR.execute(f' CREATE TABLE "qbet-{inserted_id}" ("id" INTEGER UNIQUE, "user" TEXT, "amount" int, "option" TEXT, PRIMARY KEY("id" AUTOINCREMENT))')
    CONNECTION.commit()
    return(inserted_id)

def bet_status(id):
    CURSOR.execute("SELECT status FROM dashboard WHERE id = ?",(id,))
    data = CURSOR.fetchall()
    status = data[0][0]
    return(status)

def bet_join(id, name, amount, option):
    CURSOR.execute(f'INSERT INTO "qbet-{id}" (user, amount, option) VALUES(?, ?, ?)', (name, amount, option))
    CONNECTION.commit()
    qlogs.info(f'--BET-DB // {name} JOINED qbet-{id}, betting : {amount} QC on option {option}')

def bet_close(name):
    CURSOR.execute("SELECT id FROM dashboard WHERE user = ? and status = ?",(name,"open"))
    data = CURSOR.fetchall()
    id = data[0][0]

    CURSOR.execute(f"SELECT amount FROM 'qbet-{id}' WHERE option = ?",("A",))
    data = CURSOR.fetchall()
    if (len(data)) > 0:
        listama = data[0]
        totala = sum(listama)
    else:
        totala = 0

    CURSOR.execute(f"SELECT amount FROM 'qbet-{id}' WHERE option = ?",("B",))
    data = CURSOR.fetchall()
    if (len(data)) > 0:
        listamb = data[0]
        totalb = sum(listamb)
    else:
        totalb = 0

    CURSOR.execute("UPDATE dashboard SET status = ?, total_a = ?, total_b = ? WHERE id = ?", ("close", totala, totalb, id))
    CONNECTION.commit()
    qlogs.info(f'--BET-DB // BET CLOSED by {name}')
    #SHOULD RETURN // the total number of bidders // the amount of money bet total // number of poeple betting on a // number of poeple betting on b ... // HIGHEST BIDDER
    return(totala, totalb)

def bet_has_a_bet_going_on(name):
    CURSOR.execute("SELECT COUNT(*) FROM dashboard WHERE user = ? and status != ?",(name,"result"))
    data = CURSOR.fetchall()
    return(data[0][0])

def bet_result(name, option):
    CURSOR.execute("SELECT id FROM dashboard WHERE user = ? and status != ?",(name,"result"))
    data = CURSOR.fetchall()
    id = data[0][0]

    if option == "A":
        winlet = "a"
        loslet = "b"
    else:
        winlet = "b"
        loslet = "a"
    
    CURSOR.execute(f"SELECT total_{winlet} FROM dashboard WHERE id = ?",(id,))
    data = CURSOR.fetchall()
    wintotal = data[0][0]

    CURSOR.execute(f"SELECT total_{loslet} FROM dashboard WHERE id = ?",(id,))
    data = CURSOR.fetchall()
    lostotal = data[0][0]

    CURSOR.execute(f"SELECT user, amount FROM 'qbet-{id}' WHERE option = ?",(winlet.upper(),))
    data = CURSOR.fetchall()
    for i in range(len(data)):
        user = data[i][0]
        amount = data[i][1]
        proportion = amount / wintotal
        result = amount + int(proportion * lostotal)
        qdb.add(user, result)
        qlogs.info(f'--BET-DB // ADDED {result} QC to {user} for Winning the BET')
    
    CURSOR.execute("UPDATE dashboard SET status = ? WHERE id = ?", ("result", id))
    CONNECTION.commit()
    qlogs.info(f'--BET-DB // BET RESULT by {name}')