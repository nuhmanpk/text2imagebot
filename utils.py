from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from models import MODELS

HELP = """
● Send a Prompt , Reply /generate to the Prompt to start Image Generation
"""

START_STRING = """ **Hello {}, I'm Text to Image bot**
Capable of running all Large image Generation Models from huggingface.

`Join My Updates Channel for Getting more familiar with me`

"""

ABOUT = """
● **AUTHOR :** [bughunter0](https://t.me/bughunter0) 
● **LIBRARY :** `Pyrogram` 
● **LANGUAGE :** `Python 3.10` 
● **SOURCE :** [BugHunterBots](https://github.com/nuhmanpk) 
"""

CHANNEL_BUTTON = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('↗ Join Here ↗', url='https://t.me/BughunterBots')
    ]]
)

GITHUB_BUTTON = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('↗ Source Code ↗', url='https://github.com/nuhmanpk/text2imagebot')
    ]]
)

START_BUTTON = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('ABOUT', callback_data='cbabout'),
        InlineKeyboardButton('HELP', callback_data='cbhelp')
    ],[
        InlineKeyboardButton('SETTINGS', callback_data='cbsettings')
    ]
     ,
        [
        InlineKeyboardButton(
            '↗ Join Here ↗', url='https://t.me/BughunterBots'),
    ]]

)
CLOSE_BUTTON = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('Back', callback_data='cbclose'),
    ]]
)


BACK = [
        InlineKeyboardButton('BACK', callback_data="back")
    ]


SETTINGS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Choose Model", callback_data="choose_model"),
                InlineKeyboardButton("Change Steps", callback_data="change_steps")
            ],
            [
                InlineKeyboardButton("Change Seed", callback_data="change_seed"),
                InlineKeyboardButton("Save Settings", callback_data="save_settings")
            ]
        ]
)

MODELS_BUTTON = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(model, callback_data=f"select_model_{index}")] for index, model in enumerate(MODELS)
    ]
)

STEPS_BUTTON = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("-", callback_data="-steps"),
                InlineKeyboardButton("+", callback_data="+steps")
            ],[
                InlineKeyboardButton('Back', callback_data='cbclose')]
        ]
)