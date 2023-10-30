from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


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
    ],
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