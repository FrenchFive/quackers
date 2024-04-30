import os
from datetime import datetime

import logging

scrpt_dir = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(scrpt_dir, "qlogs.log")
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s' ,filename=LOG_FILE, encoding='utf-8', level=logging.INFO)

def info(message):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: {message}')
    logging.info(message)
    return(message)

def admin(message):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} :: {message}')
    logging.critical(message)
    return(message)