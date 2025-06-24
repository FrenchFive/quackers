import random

import os
import sqlite3
from sqlite3 import Error
import time
from datetime import datetime, timedelta
import requests
import html

import qquiz

from consts import DATA_DIR, ROOT_DIR
import qlogs
import qdatabase as qdb

folder_name = 'db/qbet.db'
database_path = os.path.join(ROOT_DIR, folder_name)

CONNECTION = sqlite3.connect(database_path)
CURSOR = CONNECTION.cursor()
CURSOR.execute(' CREATE TABLE IF NOT EXISTS "dashboard" ("id" INTEGER UNIQUE, "user" TEXT, "title" TEXT, "status" TEXT, "A" TEXT, "B" TEXT, "total_a" INT, "total_b" INT, PRIMARY KEY("id" AUTOINCREMENT))')
CONNECTION.commit()

def roll(num):
    dicelist = []
    for i in range(num):
        dicelist.append(random.randint(1,6))
    return(dicelist)

def dices(guild, num, money, name):
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
        qdb.luck(guild, name, -1)
    elif usertotal > bottotal :
        response+= f'\n{name.capitalize()} WON // with {usertotal} over {bottotal}\n'
        response+= f'{money} <:quackCoin:1124255606782578698> added to {name} balance.'
        end = 1
        qdb.luck(guild, name, 1)
    else :
        response+= f'\nEGALITE !!! // with {usertotal} over {bottotal}\n'
        end = 2
    
    return(response, end)

def rps(guild, user, bet, name):
    play = ["scissors","paper","rock","lizard","spock"]
    emoji = ['✂️', '🧻', '🪨', '🦎', '🖖']
    bot = random.randint(0, len(play)-1)

    if user == bot:
        gameresult = 0
        text = "EGALITE"
    elif user+1 == bot or user-2 == bot or user+1 == bot+5 or user-2 == bot-5:
        gameresult = 1
        text = f'\n {name} a GAGNE !!! // {bet} <:quackCoin:1124255606782578698> gagnés'
        qdb.luck(guild, name, 1)
    elif bot+1 == user or bot-2 == user or bot+1 == user+5 or bot-2 == user-5:
        gameresult = -1
        text = f'\n {name} a PERDU !!! // {bet} <:quackCoin:1124255606782578698> perdus'
        qdb.luck(guild, name, -1)
    else:
        return('ERROR', 0)
    
    tosay = f'{name} a joué : {play[user]} - {emoji[user]} \n'
    tosay += f'Quackers a joué : {play[bot]} - {emoji[bot]} \n'
    tosay += text

    return(tosay, gameresult)

def hball(name):
    listwords = []
    with open(os.path.join(DATA_DIR, 'txt/hball.txt'), encoding='utf-8') as f:
        for line in f:
            listwords.append(line.strip())
    result = random.choice(listwords).replace("{user}", name)
    return(result)


def _fetch_trivia_question(difficulty: str) -> dict | None:
    """Fetch a single multiple-choice question from Open Trivia DB."""
    try:
        resp = requests.get(
            "https://opentdb.com/api.php",
            params={"amount": 1, "difficulty": difficulty, "type": "multiple"},
            timeout=10,
        )
        data = resp.json()
    except Exception:
        return None
    if data.get("response_code") != 0 or not data.get("results"):
        return None
    item = data["results"][0]
    qtext = html.unescape(item["question"])
    correct = html.unescape(item["correct_answer"])
    incorrect = [html.unescape(i) for i in item["incorrect_answers"]]
    options = incorrect + [correct]
    random.shuffle(options)
    answer_letter = "ABCD"[options.index(correct)]
    return {
        "q": qtext,
        "A": options[0],
        "B": options[1],
        "C": options[2],
        "D": options[3],
        "answer": answer_letter,
        "category": item["category"],
        "difficulty": difficulty,
    }


def generate_quiz(guild: int):
    """Generate exactly 10 unique questions for *guild*.

    The quiz includes five easy, three medium and two hard questions.
    """
    difficulties = [("easy", 5), ("medium", 3), ("hard", 2)]
    questions = []
    seen_questions = set()

    for diff, target in difficulties:
        attempts = 0
        # keep trying until we reach the desired count or hit a safety limit
        while len([q for q in questions if q["difficulty"] == diff]) < target and attempts < 50:
            attempts += 1
            q = _fetch_trivia_question(diff)
            if not q:
                continue
            category = q["category"]
            existing_global = qquiz.get_questions_by_category(category)
            existing_guild = qquiz.get_questions_by_category(category, guild)
            if (
                q["q"] in existing_global
                or q["q"] in existing_guild
                or q["q"] in seen_questions
            ):
                continue
            questions.append(q)
            seen_questions.add(q["q"])
            qlogs.info(
                f"CREATED QUESTION :: {category} [{diff}] {q['q']}"
            )
    return questions

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
        listama = []
        for i in range(len(data)):
            listama.append(data[i][0])
        totala = sum(listama)
    else:
        totala = 0

    CURSOR.execute(f"SELECT amount FROM 'qbet-{id}' WHERE option = ?",("B",))
    data = CURSOR.fetchall()
    if (len(data)) > 0:
        listamb = []
        for i in range(len(data)):
            listamb.append(data[i][0])
        totalb = sum(listamb)
    else:
        totalb = 0
    
    CURSOR.execute(f"SELECT COUNT(*) FROM 'qbet-{id}'")
    data = CURSOR.fetchall()
    totalbetter = data[0][0]

    CURSOR.execute(f"SELECT COUNT(*) FROM 'qbet-{id}' WHERE option = ?",("A",))
    data = CURSOR.fetchall()
    totalbettera = data[0][0]
    
    CURSOR.execute(f"SELECT COUNT(*) FROM 'qbet-{id}' WHERE option = ?",("B",))
    data = CURSOR.fetchall()
    totalbetterb = data[0][0]

    CURSOR.execute(f"SELECT user, option, amount FROM 'qbet-{id}' ORDER BY amount DESC LIMIT 1")
    data = CURSOR.fetchall()
    highest = data[0]

    CURSOR.execute("UPDATE dashboard SET status = ?, total_a = ?, total_b = ? WHERE id = ?", ("close", totala, totalb, id))
    CONNECTION.commit()
    qlogs.info(f'--BET-DB // BET CLOSED by {name}')
    #SHOULD RETURN // the total number of bidders // the amount of money bet total // number of poeple betting on a // number of poeple betting on b ... // HIGHEST BIDDER
    return(totala, totalb, totalbetter, totalbettera, totalbetterb, highest)

def bet_has_a_bet_going_on(name):
    CURSOR.execute("SELECT COUNT(*) FROM dashboard WHERE user = ? and status != ?",(name,"result"))
    data = CURSOR.fetchall()
    return(data[0][0])

def bet_has_betted(name, id):
    CURSOR.execute(f"SELECT COUNT(*) FROM 'qbet-{id}' WHERE user = ?",(name,))
    data = CURSOR.fetchall()
    return(data[0][0])

def bet_result(guild, name, option):
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
    if not data:
        wintotal = 0
    else:
        wintotal = data[0][0]

    CURSOR.execute(f"SELECT total_{loslet} FROM dashboard WHERE id = ?",(id,))
    data = CURSOR.fetchall()
    if not data:
        lostotal = 0
    else:
        lostotal = data[0][0]

    CURSOR.execute(f"SELECT user, amount FROM 'qbet-{id}' WHERE option = ?",(winlet.upper(),))
    data = CURSOR.fetchall()
    for i in range(len(data)):
        user = data[i][0]
        amount = data[i][1]
        proportion = amount / wintotal
        result = amount + int(proportion * lostotal)
        qdb.add(guild, user, result)
        qdb.luck(guild, user, 1)
        qlogs.info(f'--BET-DB // ADDED {result} QC to {user} for Winning the BET')
    
    CURSOR.execute(f"SELECT user FROM 'qbet-{id}' WHERE option = ?",(loslet.upper(),))
    data = CURSOR.fetchall()[0]
    for i in range(len(data)):
        user = data[i]
        qdb.luck(guild, user, -1)
    
    
    CURSOR.execute("UPDATE dashboard SET status = ? WHERE id = ?", ("result", id))
    CONNECTION.commit()
    CURSOR.execute(f"DROP table 'qbet-{id}'")
    CONNECTION.commit()
    qlogs.info(f'--BET-DB // BET RESULT by {name}')
