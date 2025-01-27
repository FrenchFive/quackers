from consts import ROOT_DIR
import sqlite3
import os

def server_check(server):
    #check that the db file exists

    if not os.path.exists(f"{ROOT_DIR}/db/quackers.db"):
        return False
    
    #check if the file has a table called server
    conn = sqlite3.connect(f"{ROOT_DIR}/db/quackers.db")
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='servers';")
    if c.fetchone() is None:
        return False
    
    #check in the table servers if the server exists
    c.execute(f"SELECT * FROM servers WHERE server_id = {server}")
    if c.fetchone() is None:
        return False

    return True