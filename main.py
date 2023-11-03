import os
import json
import io
from dotenv import load_dotenv
from pyrogram import Client, filters
from urllib.parse import quote
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import ABOUT, CLOSE_BUTTON, HELP, START_BUTTON, START_STRING, GITHUB_BUTTON, SETTINGS, MODELS_BUTTON, STEPS_BUTTON, GITHUB_LINK, IMAGE_COUNT_BUTTON
from models import MODELS
from diffusers import StableDiffusionPipeline
import torch

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


if bot_token is None or api_id is None or api_hash is None:
    raise ValueError(
        "Please set the BOT_TOKEN, API_ID, and API_HASH environment variables.")

DEFAULT_SETTINGS = {
    'model': 'digiplay/Juggernaut_final',  # change default model in env
    'steps': 100,
    'seed': -1,
    'image_count': 1
}

app = Client("text2image", bot_token=bot_token,
             api_id=int(api_id), api_hash=api_hash)

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
            text=f"Current Settings:\n🤖 Model: {settings['model']}\n🚶‍♂️ Steps: {settings['steps']}\n🌱 Seed: {settings['seed']} \n🖼️ Image Count: {settings['image_count']}",
            reply_markup=SETTINGS,
            disable_web_page_preview=True
        )
    elif update.data == "choose_model":
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        await update.message.edit_text(
            text=f"Current Settings:\n🤖 Model: {settings['model']}\n🚶‍♂️ Steps: {settings['steps']}\n🌱 Seed: {settings['seed']} \n🖼️ Image Count: {settings['image_count']}",
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
            if current_steps < 10:
                settings['steps'] = current_steps + 1
            elif current_steps < 50:
                settings['steps'] = current_steps + 10
            else:
                settings['steps'] = current_steps + 50
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Steps: {settings['steps']}",
            reply_markup=STEPS_BUTTON,
            disable_web_page_preview=True
        )
    
    elif update.data == "change_image_count":
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        await update.message.edit_text(
            text=f"The num of Images that model Produce per prompt\nImages: {settings['image_count']}",
            reply_markup=IMAGE_COUNT_BUTTON,
            disable_web_page_preview=True
        )       
    elif update.data.startswith("+image"):
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            current_image_count = settings.get('image_count')
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            settings['image_count'] = current_image_count +  1
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Images: {settings['image_count']}",
            reply_markup=IMAGE_COUNT_BUTTON,
            disable_web_page_preview=True
        )   

    elif update.data.startswith("-image"):
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            current_image_count = settings.get('image_count')
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            try:
                settings['image_count'] = current_image_count - 1 if current_image_count > 1 else 1
            except:
                pass
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Images: {settings['image_count']}",
            reply_markup=IMAGE_COUNT_BUTTON,
            disable_web_page_preview=True
        )

    elif update.data.startswith("-steps"):
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            current_steps = settings.get('steps')
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
            if current_steps > 50:
                settings['steps'] = current_steps - 50
            elif current_steps > 10:
                settings['steps'] = current_steps - 10
            elif current_steps > 1:
                settings['steps'] = current_steps - 1
        with open(settings_file_path, 'w') as f:
            json.dump(settings, f, indent=4)
        await update.message.edit_text(
            text=f"Steps: {settings['steps']}",
            reply_markup=STEPS_BUTTON,
            disable_web_page_preview=True
        )
    elif update.data.startswith("cb_back_settings"):
        with open(settings_file_path, 'r') as f:
            settings = json.load(f)
        await update.message.edit_text(
            text=f"Current Settings:\n🤖 Model: {settings['model']}\n🚶‍♂️ Steps: {settings['steps']}\n🌱 Seed: {settings['seed']} \n🖼️ Image Count: {settings['image_count']}",
            reply_markup=SETTINGS,
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
            model_loaded = await load_model(settings.get('model'), update)
            if not model_loaded:
                await update.reply_text("Failed to load the model.")
                return
            else:
                await text.edit('Generating Image...')
            try:
                images = await generate_image(prompt, settings.get("steps"), settings.get('seed'),settings.get('image_count'))
                await text.edit(f'Uploading {settings.get("image_count")} Image ....')
                for image in images:
                    await update.reply_photo(image, reply_markup=GITHUB_BUTTON)
                await text.delete()
            except Exception as e:
                await text.delete()
                text = f'Failed to generate Image \nCreate an issue here'
                error = f"ERROR: {(str(e))}"
                error_link = f"{GITHUB_LINK}/issues/new?title={quote(error)}"
                issue_markup = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Create Issue", url=error_link)]])
                await update.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
    else:
        await update.reply_text(
            text='Reply /generate to a prompt',
            disable_web_page_preview=True,
            quote=True
        )


async def load_model(model, update):
    global pipe
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            model, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        return True
    except Exception as e:
        text = f'Failed to download Model \nCreate an issue here'
        error = f"ERROR: {(str(e))}"
        error_link = f"{GITHUB_LINK}/issues/new?title={quote(error)}"
        issue_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Create Issue", url=error_link)]])
        await update.reply_text(text, disable_web_page_preview=True, quote=True, reply_markup=issue_markup)
        return False


async def generate_image(prompt, steps, seed, count):
    global pipe
    steps = steps
    if seed == -1:
        torch.manual_seed(torch.seed())
    else:
        torch.manual_seed(seed)
    pipe = pipe.to("cuda")
    images = pipe(prompt, num_inference_steps=steps,num_images_per_prompt=count).images
    image_streams=[]
    for image in images:
        image_stream = io.BytesIO()
        image.save(image_stream, format='PNG')
        image_stream.seek(0)
        image_streams.append(image_stream)
    return image_streams


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
            text = f"Current Settings:\n🤖 Model: {model}\n🔄 Steps: {steps}"
            await update.reply_text(
                text=text,
                reply_markup=SETTINGS,
                quote=True
            )


app.run(print('Bot Running....'))