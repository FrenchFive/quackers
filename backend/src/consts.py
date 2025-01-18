import os

DATA_DIR: str = os.path.realpath(path=os.path.join(os.path.dirname(p=__file__), "../data"))
IMG_DIR: str = os.path.join(DATA_DIR, "imgs")
FONT_DIR: str = os.path.join(DATA_DIR, "fonts")
ROOT_DIR: str = os.path.realpath(path=os.path.join(os.path.dirname(p=__file__), "../.."))
