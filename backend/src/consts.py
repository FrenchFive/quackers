import os

DATA_DIR: str = os.path.realpath(os.path.join(os.path.dirname(p=__file__), "../data"))
IMG_DIR: str = os.path.join(DATA_DIR, "imgs")
FONT_DIR: str = os.path.join(DATA_DIR, "fonts")
BADGE_DIR: str = os.path.join(IMG_DIR, "badges")
ROOT_DIR: str = os.path.realpath(os.path.join(os.path.dirname(p=__file__), "../.."))
