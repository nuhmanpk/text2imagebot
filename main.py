import os
from pyrogram import Client, filters
from pyrogram.types import Message
from uilts import ABOUT, CLOSE_BUTTON, HELP, START_BUTTON, START_STRING, GITHUB_BUTTON
import os
import io
from dotenv import load_dotenv
from urllib.parse import quote
import os
from diffusers import StableDiffusionPipeline
import torch

load_dotenv()


bot_token = os.getenv('BOT_TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')


if bot_token is None or api_id is None or api_hash is None:
    raise ValueError(
        "Please set the BOT_TOKEN, API_ID, and API_HASH environment variables.")

app = Client("text2image", bot_token=bot_token,
             api_id=int(api_id), api_hash=api_hash)



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
async def start(bot, update):
    text = START_STRING.format(update.from_user.mention)
    reply_markup = START_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@app.on_message(filters.command(["generate"]) & filters.private)
async def generate(bot, update:Message):
    if update.reply_to_message:
        text = await update.reply_text("Generating Image...\nThis process may take time according to your Computational Power", quote=True)
        prompt = update.reply_to_message.text
        image = await generate_image(prompt)
        await text.edit('Uploading Image ....')
        await update.reply_photo(image,reply_markup=GITHUB_BUTTON)
        await text.delete()
    else:
        await update.reply_text(
            text='Reply /generate to a prompt',
            disable_web_page_preview=True,
            quote=True
        )
        
async def generate_image(prompt):
    # TODO: add multi model options
    model_id = "prompthero/openjourney" # change model name here , choose any model from huggingface
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")
    steps=200
    image = pipe(prompt,num_inference_steps=steps).images[0]
    image_stream = io.BytesIO()
    image.save(image_stream, format='PNG')
    image_stream.seek(0)
    return image_stream

app.run(print('Bot Running....'))