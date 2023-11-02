import os
import json
import io
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import ABOUT, CLOSE_BUTTON, HELP, START_BUTTON, START_STRING, GITHUB_BUTTON
from models import MODELS
import random
from diffusers import StableDiffusionPipeline
import torch

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

if bot_token is None or api_id is None or api_hash is None:
    raise ValueError("Please set the BOT_TOKEN, API_ID, and API_HASH environment variables.")

DEFAULT_SETTINGS = {
    'model': random.choice(MODELS),
    'steps': 100,
    'seed': -1
}

app = Client("text2image", bot_token=bot_token, api_id=int(api_id), api_hash=api_hash)

@app.on_callback_query()
async def cb_data(bot, update):
    if update.data == "cbhelp":
        await update.message.edit_text(
            text=HELP,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data == "cbabout":
        await update.message.edit_text(
            text=ABOUT,
            reply_markup=CLOSE_BUTTON,
            disable_web_page_preview=True
        )
    else:
        await update.message.edit_text(
            text=START_STRING.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTON
        )

@app.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update: Message):
    chat_id = update.chat.id
    settings_file_path = f'{chat_id}-settings.json'
    if not os.path.exists(settings_file_path):
        with open(settings_file_path, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)

    text = START_STRING.format(update.from_user.mention)
    reply_markup = START_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )

@app.on_message(filters.command(["generate"]) & filters.private)
async def generate(bot, update: Message):
    if update.reply_to_message:
        chat_id = update.chat.id
        text = await update.reply_text("Loading settings...", quote=True)
        prompt = update.reply_to_message.text
        with open(f'{chat_id}-settings.json') as f:
            settings = json.load(f)
            await text.edit('Settings Loaded...')
            await text.edit(f'Downloading...\n{settings.get("model")}')
            model_loaded = await load_model(settings.get('model'))
            if not model_loaded:
                await update.reply_text("Failed to load the model.")
                return

            image = await generate_image(prompt, settings.get("steps"))
            await text.edit('Uploading Image ....')
            await update.reply_photo(image, reply_markup=GITHUB_BUTTON)
            await text.delete()
    else:
        await update.reply_text(
            text='Reply /generate to a prompt',
            disable_web_page_preview=True,
            quote=True
        )

async def load_model(model):
    global pipe
    try:
        pipe = StableDiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        return True
    except Exception as e:
        print(e)
        return False

async def generate_image(prompt, steps):
    global pipe
    steps = steps
    pipe = pipe.to("cuda")
    image = pipe(prompt, num_inference_steps=steps).images[0]
    image_stream = io.BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream

app.run(print('Bot Running....'))