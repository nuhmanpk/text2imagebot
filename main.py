import os
import json
import io
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import ABOUT, CLOSE_BUTTON, HELP, START_BUTTON, START_STRING, GITHUB_BUTTON, SETTINGS, MODELS_BUTTON, STEPS_BUTTON
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

pipe = None

@app.on_callback_query()
async def cb_data(bot, update):
    chat_id = update.message.chat.id
    settings_file_path = f'{chat_id}-settings.json'
    if not os.path.exists(settings_file_path):
        with open(settings_file_path, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
            
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
    elif update.data == "cbsettings":
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        await update.message.edit_text(
            text=f'Current Settings\n{settings}',
            reply_markup=SETTINGS,
            disable_web_page_preview=True
        )
    elif update.data == "choose_model":
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        await update.message.edit_text(
            text=f'Current Settings\n{settings}',
            reply_markup=MODELS_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data.startswith("select_model_"):
        index = int(update.data.split("_")[2])
        selected_model = MODELS[index]
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        settings['model'] = selected_model
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Selected model: {selected_model}",
            reply_markup=SETTINGS,
            disable_web_page_preview=True
        )
    elif update.data == "change_steps":
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        await update.message.edit_text(
                text=f"Steps: {settings['steps']}",
                reply_markup=STEPS_BUTTON,
                disable_web_page_preview=True
            )
    elif update.data.startswith("+steps"):
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            current_steps = settings.get('steps')
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            settings['steps'] = current_steps+50
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Steps: {settings['steps']}",
            reply_markup=STEPS_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data.startswith("-steps"):
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            current_steps = settings.get('steps')
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            try:
                settings['steps'] = current_steps - 50 if current_steps > 50 else 50
            except:
                pass
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Steps: {settings['steps']}",
            reply_markup=STEPS_BUTTON,
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
        settings_file_path = f'{chat_id}-settings.json'
        if not os.path.exists(settings_file_path):
            with open(settings_file_path, 'w') as f:
                json.dump(DEFAULT_SETTINGS, f, indent=4)
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
            else:
                await text.edit('Generating Image...')
            image = await generate_image(prompt, settings.get("steps"),settings.get('seed'))
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


async def generate_image(prompt, steps, seed):
    global pipe
    steps = steps
    if seed == -1:
        torch.manual_seed(torch.seed())
    else:
        torch.manual_seed(seed)
    pipe = pipe.to("cuda")
    image = pipe(prompt, num_inference_steps=steps).images[0]
    image_stream = io.BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream

@app.on_message(filters.command(["settings"]) & filters.private)
async def settings(bot, update: Message):
    chat_id = update.chat.id
    settings_file_path = f'{chat_id}-settings.json'
    if not os.path.exists(settings_file_path):
        with open(settings_file_path, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4)
            text = "Settings file created. Please use the command again to access the settings."
    else:
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            model = settings.get('model')
            steps = settings.get('steps')
            text = f"Current Settings:\nModel: {model}\nSteps: {steps}"



    await update.reply_text(
        text=text,
        reply_markup=SETTINGS,
        quote=True
    )

app.run(print('Bot Running....'))