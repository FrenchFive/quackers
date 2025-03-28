import os
from datetime import datetime

import logging

from consts import ROOT_DIR

LOG_FILE = os.path.join(ROOT_DIR, "qlogs.log")

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s' ,filename=LOG_FILE, encoding='utf-8', level=logging.INFO)

def info(message):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: {message}')
    logging.info(message)
    return(message)

def admin(message):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: {message}')
    logging.critical(message)
    return(message)

def error(message):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: {message}')
    logging.error(message)
    return(message)

def clear():
    with open(LOG_FILE, 'w'):
        pass