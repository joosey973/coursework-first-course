__all__ = []
import os

from dotenv import load_dotenv


load_dotenv()
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "")
COLOR_THEME = os.environ.get("COLOR_THEME", "black")

if COLOR_THEME != "black":
    COLOR_THEME = "white"


def update_colors():
    global BORDER_COLOR, BACKGROUNG_COLOR, BUTTON_COLOR, HOVER_BUTTON_COLOR
    global BACKGROUND_FRAME, TEXT_COLOR_IN_BTN, TEXT_COLOR_IN_FRAME
    global BACKGROUND_FIELD_COLOR, LISTBOX_COLOR, TEXT_COLOR
    if COLOR_THEME == "black":
        BORDER_COLOR = "#565a5d"
        BACKGROUNG_COLOR = "#323232"
        BUTTON_COLOR = "#fce566"
        HOVER_BUTTON_COLOR = "#d7c662"
        BACKGROUND_FRAME = "#2b2b2b"
        TEXT_COLOR_IN_BTN = "#353638"
        TEXT_COLOR_IN_FRAME = "#ececec"
        BACKGROUND_FIELD_COLOR = "#353638"
        LISTBOX_COLOR = "#000000"
    else:
        BACKGROUNG_COLOR = "#ececec"
        BACKGROUND_FIELD_COLOR = "#f9f9fa"
        BACKGROUND_FRAME = "#dbdadb"
        TEXT_COLOR_IN_FRAME = "#000000"
        TEXT_COLOR = "#ececec"
        TEXT_COLOR_IN_BTN = "#ececec"
        BUTTON_COLOR = "#36719f"
        HOVER_BUTTON_COLOR = "#2d5a7b"
        BORDER_COLOR = "#979da3"
        LISTBOX_COLOR = "#ffffff"


update_colors()
