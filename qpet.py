import os
import sqlite3
from sqlite3 import Error
import time
import random

import qlogs

SCRPTDITR = os.path.dirname(os.path.abspath(__file__))
folder_name = 'db/qpet.db'
database_path = os.path.join(SCRPTDITR, folder_name)
folder_name = 'db/quserpet.db'
userdatabase_path = os.path.join(SCRPTDITR, folder_name)

PETDATA = sqlite3.connect(database_path)
CURSORDATA = PETDATA.cursor()
CURSORDATA.execute('''
CREATE TABLE IF NOT EXISTS "accessories" (
    "id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"path"	TEXT NOT NULL,
	"position"	TEXT NOT NULL,
    "price" INT NOT NULL,
	PRIMARY KEY("id")
);
''')
PETDATA.commit()

CONNECTION = sqlite3.connect(userdatabase_path)
CURSOR = CONNECTION.cursor()
CURSOR.execute('''
CREATE TABLE IF NOT EXISTS "dashboard" (
	"user"	TEXT NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "xp" INT,
    "body" TEXT,
    "eyes" TEXT,
    "back" TEXT,
    "hand_left" TEXT,
    "hands_right" TEXT,
    "hat" TEXT,
	PRIMARY KEY("user")
);
''')
CONNECTION.commit()