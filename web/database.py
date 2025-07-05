from .consts import ROOT_DIR, TXT_DIR
import sqlite3
import os
import qlogs

def server_check(server, name):
    #check that the db file exists

    if not os.path.exists(f"{ROOT_DIR}/db/quackers.db"):
        return "Database file not found. Please contact the bot owner and RUN the bot once to initiate files."
    
    #check if the file has a table called server
    conn = sqlite3.connect(f"{ROOT_DIR}/db/quackers.db")
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='servers';")
    if c.fetchone() is None:
        return "Database file found, but the table 'servers' is missing. Please contact the bot owner and RUN the bot once to initiate files."
    
    #check in the table servers if the server exists
    c.execute(f"SELECT * FROM servers WHERE server_id = {server}")
    if c.fetchone() is None:
        connec = sqlite3.connect(f"{ROOT_DIR}/db/quackers.db")
        cursor = connec.cursor()
        cursor.execute('INSERT INTO servers (server_id, server_name) VALUES(?, ?)', (server, name))
        connec.commit()
        connec.close()

    return None

def get_server_info(guild):
    conn = sqlite3.connect(f"{ROOT_DIR}/db/quackers.db")
    conn.row_factory = sqlite3.Row  # This allows accessing rows as dictionaries
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM servers WHERE server_id = ?", (guild,))
    result = cursor.fetchone()

    conn.close()

    results = dict(result)
    return results

def update_server_info(guild, parm, value):
    conn = sqlite3.connect(f"{ROOT_DIR}/db/quackers.db")
    cursor = conn.cursor()

    cursor.execute(f"UPDATE servers SET {parm} = ?, nsync = 1 WHERE server_id = ?", (value, guild))
    conn.commit()

    qlogs.info(f"Server {guild} updated {parm} -> {value} (nsync set)")

    conn.close()

def get_txt(file):
    with open(f"{TXT_DIR}/{file}.txt", "r", encoding="utf-8") as f:
        txt = f.read()
    return txt
