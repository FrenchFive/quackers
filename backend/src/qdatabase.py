import os
from datetime import datetime, timedelta
import sqlite3
from sqlite3 import Error
import json
import time
import random
import shutil

from consts import ROOT_DIR
import qlogs

DB_PATH = os.path.join(ROOT_DIR, 'db/quackers.db')
STATS_PATH = os.path.join(ROOT_DIR, 'db/stats.db')

CONNECTION = sqlite3.connect(DB_PATH)
CURSOR = CONNECTION.cursor()

STATS_CONNECTION = sqlite3.connect(STATS_PATH)
STATS_CURSOR = STATS_CONNECTION.cursor()

CURSOR.execute('''
CREATE TABLE IF NOT EXISTS "servers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, 
    "server_id" INTEGER UNIQUE NOT NULL, 
    "server_name" TEXT NOT NULL, 
    "lang" TEXT DEFAULT 'eng',
    
    "admin_role_id" INTEGER DEFAULT 0,
    "admin_ch_id" INTEGER DEFAULT 0,
    "gnrl_ch_id" INTEGER DEFAULT 0,
    "dbg_ch" BOOLEAN DEFAULT 0,
    "dbg_ch_id" INTEGER DEFAULT 0,
    "bot_ch_id" INTEGER DEFAULT 0,

    "wlc" BOOLEAN DEFAULT 0,
    "wlc_ch_id" INTEGER DEFAULT 0,
    "wlc_msg" BOOLEAN DEFAULT 0,
    "wlc_msg_content" TEXT DEFAULT '',
    "wlc_rct" BOOLEAN DEFAULT 0,
    "wlc_rct_cstm" BOOLEAN DEFAULT 1,

    "gdb" BOOLEAN DEFAULT 0,
    "gdb_ch_id" INTEGER DEFAULT 0,
    "gdb_msg_content" TEXT DEFAULT '',

    "prst" BOOLEAN DEFAULT 0,
    "prst_ch_id" INTEGER DEFAULT 0,
    "prst_role" INTEGER DEFAULT 0,

    "dm" BOOLEAN DEFAULT 0,
    "dm_msg_content" TEXT DEFAULT '',

    "eco" BOOLEAN DEFAULT 0,
    "eco_pss" BOOLEAN DEFAULT 1,
    "eco_pss_msg" BOOLEAN DEFAULT 1,
    "eco_pss_msg_value" INTEGER DEFAULT 1,
    "eco_pss_ch" BOOLEAN DEFAULT 1,
    "eco_pss_ch_value" INTEGER DEFAULT 15,
    "eco_pss_ch_afk" BOOLEAN DEFAULT 0,
    "eco_pss_ch_afk_id" INTEGER DEFAULT 0,
    "eco_pss_cmd" BOOLEAN DEFAULT 1,
    "eco_pss_cmd_value" INTEGER DEFAULT 5,

    "bnk" BOOLEAN DEFAULT 0,
    "bnk_itrs" BOOLEAN DEFAULT 1,
    "bnk_itrs_value" INTEGER DEFAULT 30,

    "snd" BOOLEAN DEFAULT 0,
    "snd_limit" BOOLEAN DEFAULT 0,
    "snd_limit_value" INTEGER DEFAULT 100,

    "dly" BOOLEAN DEFAULT 0,
    "dly_from_value" INTEGER DEFAULT 100,
    "dly_to_value" INTEGER DEFAULT 250,
    "dly_random" BOOLEAN DEFAULT 1,

    "game" BOOLEAN DEFAULT 0,
    "game_limit" BOOLEAN DEFAULT 1,
    "game_limit_value" INTEGER DEFAULT 100,

    "dices" BOOLEAN DEFAULT 0,
    "rps" BOOLEAN DEFAULT 0,
    "hball" BOOLEAN DEFAULT 0,
    "bet" BOOLEAN DEFAULT 0,
    "bet_limit" BOOLEAN DEFAULT 0,
    "bet_limit_value" INTEGER DEFAULT 1000,

    "ai_chat" BOOLEAN DEFAULT 0,
    "ai_img" BOOLEAN DEFAULT 0,
    "ai_img_pay" BOOLEAN DEFAULT 1,
    "ai_img_pay_value" INTEGER DEFAULT 100
);
''')

#SERVERS
def get_all_server_ids():
    # Query the database for all server IDs
    CURSOR.execute('SELECT server_id FROM servers')
    rows = CURSOR.fetchall()
    
    # Extract the server IDs from the query results
    server_ids = [row[0] for row in rows]
    
    return server_ids

def add_server(guild, name):
    if guild in get_all_server_ids():
        return
    CURSOR.execute('INSERT INTO servers (server_id, server_name) VALUES(?, ?)', (guild, name))
    CONNECTION.commit()
    qlogs.info(f'--QDB // ADDED SERVER : {name} :: {guild}')

def servers_table_exists(guild):
    CURSOR.execute(f'''CREATE TABLE IF NOT EXISTS "{guild}" (
        "id" INTEGER UNIQUE, 
        "name" TEXT, 
        "coins" INTEGER, 
        "daily" TEXT, 
        "quackers" INTEGER, 
        "mess" INTEGER, 
        "created" TEXT, 
        "streak" INTEGER DEFAULT 0, 
        "epvoicet" INTEGER DEFAULT 0, 
        "voiceh" INTEGER DEFAULT 0, 
        "luck" INTEGER DEFAULT 0, 
        "bank" INTEGER DEFAULT 0, 
        PRIMARY KEY("id" AUTOINCREMENT)
    );''')
    CONNECTION.commit()

def get_server_info(guild, info):
    CURSOR.execute(f'SELECT {info} FROM servers WHERE server_id = ?', (guild,))
    result = CURSOR.fetchone()
    return result

#MEMBERS
def user_in_db(guild, member):
    if member.bot:
        return  0# Skip adding bots

    name = member.name

    CURSOR.execute(f"SELECT COUNT(*) FROM '{guild}' WHERE name = ?",(name,))
    data = CURSOR.fetchall()
    result = data[0][0]

    if result == 0:
        # Add the user to the database
        date = member.joined_at.strftime('%Y-%m-%d %H:%M')
        CURSOR.execute(f'INSERT INTO "{guild}" (name, coins, daily, quackers, mess, created, streak, epvoicet, voiceh, luck, bank) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (name, 0, "", 0, 0, date, 0, 0, 0, 0, 0))
        CONNECTION.commit()
        qlogs.info(f'--QDB // ADDED USER : {name} :: to {guild}')
    
    return 1

def coins(guild, name):
    CURSOR.execute(f"SELECT coins FROM '{guild}' WHERE name = ?", (name,))
    data = CURSOR.fetchall()
    return(f'{name.capitalize()} possède {data[0][0]} <:quackCoin:1124255606782578698>.')

def qcheck(guild, name, amount):
    CURSOR.execute(f"SELECT coins FROM '{guild}' WHERE name = ?",(name,))
    data = CURSOR.fetchall()
    coins = data[0][0]

    if coins >= amount:
        return(0)
    else:
        return(1)

def add(guild, name, amount):
    CURSOR.execute(f"SELECT coins FROM '{guild}' WHERE name = ?",(name,))
    rows = CURSOR.fetchall()
    data = rows[0]
    coins = data[0]

    coins += amount

    CURSOR.execute(f"UPDATE '{guild}' SET coins = ? WHERE name = ?", (coins, name))
    CONNECTION.commit()

def luck(guild, name, amount):
    CURSOR.execute(f"SELECT luck FROM '{guild}' WHERE name = ?",(name,))
    rows = CURSOR.fetchall()
    data = rows[0]
    luck = data[0]

    luck += amount

    CURSOR.execute(f"UPDATE '{guild}' SET luck = ? WHERE name = ?", (luck, name))
    CONNECTION.commit()          

def add_mess(guild, name):
    CURSOR.execute(f"SELECT mess FROM '{guild}' WHERE name = ?",(name,))
    data = CURSOR.fetchall()
    mess = data[0][0]

    mess += 1

    CURSOR.execute(f"UPDATE '{guild}' SET mess = ? WHERE name = ?", (mess, name))
    CONNECTION.commit()

def add_quackers(guild, name):
    CURSOR.execute(f"SELECT quackers FROM '{guild}' WHERE name = ?",(name,))
    data = CURSOR.fetchall()
    quackers = data[0][0]

    quackers += 1

    CURSOR.execute(f"UPDATE '{guild}' quackers = ? WHERE name = ?", (quackers, name))
    CONNECTION.commit()

def daily(guild, name):
    date = datetime.now().strftime('%Y-%m-%d')
    CURSOR.execute(f"SELECT coins, daily, streak FROM '{guild}' WHERE name = ?",(name,))
    rows = CURSOR.fetchall()
    data = rows[0]
    coins = data[0]
    daily = data[1]
    streak = data[2]

    if daily != date:
        amount = 100
        if daily == (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'):
            streak += 1
            if streak > 20:
                amount = random.randint(250, 350)
            else:
                mult = 1 + (streak - 1) * (2.5 - 1) / (20 - 1)
                amount *= mult
            
        else:
            streak = 0

        coins += int((amount))

        CURSOR.execute(f"UPDATE '{guild}' SET coins = ?, daily = ?, streak = ? WHERE name = ?", (coins, date, streak, name))
        CONNECTION.commit()
        qlogs.info(f'--QDB // DAILY : {name} : {coins}')
        if streak == 0:
            return(f'Successfully added {int((amount))} <:quackCoin:1124255606782578698> to {name} balance, total : {coins} QuackCoins')
        else:
            return(f'Successfully added {int((amount))} <:quackCoin:1124255606782578698> to {name} balance, total : {coins} QuackCoins // STREAK : {streak}')
    else:
        return(f'Daily QuackCoins have already been collected today for {name}')

def send(guild, fname, dname, amount):
    if amount<0:
        return('The amount must be higher than 1 <:quackCoin:1124255606782578698>.')
    CURSOR.execute(f"SELECT coins FROM '{guild}' WHERE name = ?",(fname,))
    data = CURSOR.fetchall()
    fcoin = data[0][0]
    if fcoin < amount:
        return("INSUFFICIENT FUNDS")
    
    CURSOR.execute(f"UPDATE '{guild}' SET coins = ? WHERE name = ?", (fcoin-amount, fname))
    CONNECTION.commit()
    CURSOR.execute(f"SELECT coins FROM '{guild}' WHERE name = ?",(dname,))
    data = CURSOR.fetchall()
    dcoin = data[0][0]
    CURSOR.execute(f"UPDATE '{guild}' SET coins = ? WHERE name = ?", (dcoin+amount, dname))
    CONNECTION.commit()
    qlogs.info(f'--QDB // SENT : {amount} // FROM : {fname} / TO : {dname} - GUILD :: {guild}')
    return(f"{fname.capitalize()} sent {amount} <:quackCoin:1124255606782578698> to {dname.capitalize()}")

def bank(guild, name):
    CURSOR.execute(f"SELECT coins FROM '{guild}' WHERE name = ?", (name,))
    data = CURSOR.fetchall()
    coins = data[0][0]
    CURSOR.execute(f"SELECT bank FROM '{guild}' WHERE name = ?", (name,))
    data = CURSOR.fetchall()
    bank = data[0][0]
    return coins, bank

def bank_deposit(guild, name, amount):
    CURSOR.execute(f"SELECT coins, bank FROM '{guild}' WHERE name = ?", (name,))
    data = CURSOR.fetchall()
    coins = data[0][0]
    bank = data[0][1]
    if coins < amount:
        return(f"Vous n'avez pas assez de <:quackCoin:1124255606782578698> pour déposer {amount}.")
    else:
        coins -= amount
        bank += amount
        CURSOR.execute(f"UPDATE '{guild}' SET coins = ?, bank = ? WHERE name = ?", (coins, bank, name))
        CONNECTION.commit()
        return(f"Vous avez déposé {amount} <:quackCoin:1124255606782578698> dans votre compte en banque.")

def bank_withdraw(guild, name, amount):
    CURSOR.execute(f"SELECT coins, bank FROM '{guild}' WHERE name = ?", (name,))
    data = CURSOR.fetchall()
    coins = data[0][0]
    bank = data[0][1]
    if bank < amount:
        return(f"Vous n'avez pas assez de <:quackCoin:1124255606782578698> dans votre compte en banque pour retirer {amount}.")
    else:
        coins += amount
        bank -= amount
        CURSOR.execute(f"UPDATE '{guild}' SET coins = ?, bank = ? WHERE name = ?", (coins, bank, name))
        CONNECTION.commit()
        return(f"Vous avez retiré {amount} <:quackCoin:1124255606782578698> de votre compte en banque.")

def bank_update(guild, interest):
    #Update the bank trust fund 
    CURSOR.execute(f"SELECT name, bank FROM '{guild}'")
    data = CURSOR.fetchall()
    for i in range(len(data)):
        name = data[i][0]
        bank = data[i][1]
        if bank > 0:
            bank += int(bank * (interest / 100))
            CURSOR.execute(f"UPDATE '{guild}' SET bank = ? WHERE name = ?", (bank, name))
            CONNECTION.commit()
            qlogs.info(f'-- QDB // Added {int(bank * (interest / 100))} to {name} bank account. :: GUILD :: {guild}')

def info(guild, name):
    CURSOR.execute(f"SELECT coins, bank, mess, created, epvoicet, voiceh, luck FROM '{guild}' WHERE name = ?", (name,))
    data = CURSOR.fetchall()

    coins = data[0][0]
    bank = data[0][1]
    CURSOR.execute(f"SELECT COUNT(*) FROM '{guild}' WHERE (coins + bank) > ?",((coins+bank),))
    cdata = CURSOR.fetchall()
    rank = cdata[0][0] + 1
    return(data[0], rank)

def leaderboard(guild):
    CURSOR.execute(f"SELECT name, coins, bank FROM '{guild}' ORDER BY (coins + bank) DESC LIMIT 10")
    data = CURSOR.fetchall()
    result = []
    emoji = ["🥇","🥈","🥉",""]
    for i in range(len(data)):
        emo = i
        if i >= 3:
            emo = 3
        bold = ""
        if i <= 2:
            bold = "**"
        result.append(f'{emoji[emo]} N.{i+1} :: {bold}{data[i][0].capitalize()}{bold} :: {(data[i][1] + data[i][2])} <:quackCoin:1124255606782578698>')
    return(result)

def voiceactive(guild, name):
    timenow = int(time.time())
    CURSOR.execute(f"UPDATE '{guild}' SET epvoicet = ? WHERE name = ?",(timenow, name))
    CONNECTION.commit()

def voicestalled(guild, name):
    timenow = int(time.time())
    CURSOR.execute(f"SELECT epvoicet FROM '{guild}' WHERE name = ?",(name,))
    data = CURSOR.fetchall()
    past = data[0][0]
    hours = 0

    if past != 0 and past < timenow:
        secelapsed = timenow - past
        if secelapsed > 3600:
            hours = divmod(secelapsed, 3600)[0]
            amount = 50 * hours
            if amount > 500:
                amount = 500
            add(guild, name, amount)
            #ADD HOURS TO DB
            CURSOR.execute(f"SELECT voiceh FROM '{guild}' WHERE name = ?",(name,))
            raw = CURSOR.fetchall()
            data = raw[0][0]

            data += hours

            CURSOR.execute(f"UPDATE '{guild}' SET voiceh = ? WHERE name = ?", (data, name))
            CONNECTION.commit()
            #LOGS
            qlogs.info(f"-- QDB // Added {amount} to {name} for being active in Voice Channel.")

    CURSOR.execute(f"UPDATE '{guild}' SET epvoicet = ? WHERE name = ?",(0, name))
    CONNECTION.commit()

    return hours

#STATS
def add_stat(guild, user, type, amount):
    weekday_number = datetime.now().weekday()
    # check if a table exists with the id of the guild as tables name
    STATS_CURSOR.execute(f"CREATE TABLE IF NOT EXISTS '{guild}' (id INTEGER PRIMARY KEY AUTOINCREMENT, time INT, name TEXT, type TEXT, amount INTEGER)")
    STATS_CONNECTION.commit()

    # insert the data into the table
    STATS_CURSOR.execute(f"INSERT INTO '{guild}' (time, name, type, amount) VALUES (?, ?, ?, ?)", (weekday_number, user, type, amount))
    STATS_CONNECTION.commit()

def get_stats(guild):
    # Total of each different unique type
    STATS_CURSOR.execute(f"SELECT type, COUNT(*) as count FROM '{guild}' GROUP BY type")
    type_totals = STATS_CURSOR.fetchall()

    # Min and max for each different unique type
    STATS_CURSOR.execute(f"""
        SELECT type, MIN(amount) as min_amount, MAX(amount) as max_amount,
               (SELECT name FROM '{guild}' WHERE type = t.type ORDER BY amount ASC LIMIT 1) as min_author,
               (SELECT name FROM '{guild}' WHERE type = t.type ORDER BY amount DESC LIMIT 1) as max_author
        FROM '{guild}' t
        GROUP BY type
    """)
    type_min_max = STATS_CURSOR.fetchall()

    # Number of unique names in the entire database
    STATS_CURSOR.execute(f"SELECT COUNT(DISTINCT name) FROM '{guild}'")
    unique_names_count = STATS_CURSOR.fetchone()[0]

    # Total for each day
    interval_totals = [0] * 7  # Initialize a list with 7 zeros, one for each day of the week
    STATS_CURSOR.execute(f"SELECT time, COUNT(*) as count FROM '{guild}' GROUP BY time")
    for row in STATS_CURSOR.fetchall():
        day_of_week, count = row
        interval_totals[day_of_week] = count
    


    # Name who has the most entries for each type
    STATS_CURSOR.execute(f"SELECT type, name, COUNT(*) as count FROM '{guild}' GROUP BY type, name ORDER BY type, count DESC")
    type_most_entries = {}
    for row in STATS_CURSOR.fetchall():
        type, name, count = row
        if type not in type_most_entries:
            type_most_entries[type] = name

    '''
    return {
        "type_totals": type_totals,
        "type_min_max": type_min_max,
        "unique_names_count": unique_names_count,
        "interval_totals": interval_totals
    }
    '''

    return type_totals, type_min_max, unique_names_count, interval_totals, type_most_entries

def clear_stats(guild):
    STATS_CURSOR.execute(f"DROP TABLE '{guild}'")
    STATS_CONNECTION.commit()

def backup_db():
    bckup_path = os.path.join(ROOT_DIR, "db/backup/")
    bckup_file = os.path.join(backup_db, "bckup_quackers.db")

    os.makedirs(bckup_path, exist_ok=True)

    shutil.copy(DB_PATH, bckup_file)
    qlogs.info(f"BACKUP OF THE DATABASE")
