import os
import json
from utils import (
    ABOUT,
    CLOSE_BUTTON,
    HELP,
    START_BUTTON,
    START_STRING,
    SETTINGS,
    MODELS_BUTTON,
    STEPS_BUTTON,
    IMAGE_COUNT_BUTTON,
)


async def help_callback(update):
    await update.message.edit_text(
        text=HELP, reply_markup=CLOSE_BUTTON, disable_web_page_preview=True
    )


async def about_callback(update):
    await update.message.edit_text(
        text=ABOUT, reply_markup=CLOSE_BUTTON, disable_web_page_preview=True
    )


async def settings_callback(update, settings):
    await update.message.edit_text(
        text=f"""Current Settings:\n🤖 Model: {settings['model']}\n🚶‍♂️ Steps: {settings['steps']}\n
        🌱 Seed: {settings['seed']} \n
        🖼️ Image Count: {settings['image_count']}""",
        reply_markup=SETTINGS,
        disable_web_page_preview=True,
    )


async def choose_model_callback(update, settings):
    await update.message.edit_text(
        text=f"""Current Settings:\n🤖 Model: {settings['model']}\n🚶‍♂️ Steps: {settings['steps']}\n
        🌱 Seed: {settings['seed']} \n
        🖼️ Image Count: {settings['image_count']}""",
        reply_markup=MODELS_BUTTON,
        disable_web_page_preview=True,
    )


async def selected_model_callback(update, selected_model, settings, settings_file_path):
    settings["model"] = selected_model
    with open(settings_file_path, "w") as f:
        json.dump(settings, f, indent=4)
    await update.message.edit_text(
        text=f"Selected model: {selected_model}",
        reply_markup=SETTINGS,
        disable_web_page_preview=True,
    )


async def change_steps_callback(update, settings):
    await update.message.edit_text(
        text=f"Steps: {settings['steps']}",
        reply_markup=STEPS_BUTTON,
        disable_web_page_preview=True,
    )


async def step_incre_callback(update, settings, settings_file_path):
    current_steps = settings.get("steps")
    if current_steps < 10:
        settings["steps"] = current_steps + 2
    elif current_steps < 50:
        settings["steps"] = current_steps + 10
    else:
        settings["steps"] = current_steps + 50
    with open(settings_file_path, "w") as f:
        json.dump(settings, f, indent=4)
    await update.message.edit_text(
        text=f"Steps: {settings['steps']}",
        reply_markup=STEPS_BUTTON,
        disable_web_page_preview=True,
    )


async def step_decre_callback(update, settings, settings_file_path):
    current_steps = settings.get("steps")
    if current_steps > 50:
        settings["steps"] = current_steps - 50
    elif current_steps > 10:
        settings["steps"] = current_steps - 10
    elif current_steps > 1:
        settings["steps"] = current_steps - 1
    with open(settings_file_path, "w") as f:
        json.dump(settings, f, indent=4)
    await update.message.edit_text(
        text=f"Steps: {settings['steps']}",
        reply_markup=STEPS_BUTTON,
        disable_web_page_preview=True,
    )


async def change_image_count_callback(update, settings):
    await update.message.edit_text(
        text=f"The num of Images that model Produce per prompt\nImages: {settings['image_count']}",
        reply_markup=IMAGE_COUNT_BUTTON,
        disable_web_page_preview=True,
    )


async def image_incre_callback(update, settings, settings_file_path):
    current_image_count = settings.get("image_count")
    with open(settings_file_path, "r") as f:
        settings = json.load(f)
        settings["image_count"] = current_image_count + 1
    with open(settings_file_path, "w") as f:
        json.dump(settings, f, indent=4)
    await update.message.edit_text(
        text=f"Images: {settings['image_count']}",
        reply_markup=IMAGE_COUNT_BUTTON,
        disable_web_page_preview=True,
    )


async def image_decre_callback(update, settings, settings_file_path):
    current_image_count = settings.get("image_count")
    try:
        settings["image_count"] = (
            current_image_count - 1 if current_image_count > 1 else 1
        )
    except:
        pass
    with open(settings_file_path, "w") as f:
        json.dump(settings, f, indent=4)
    await update.message.edit_text(
        text=f"Images: {settings['image_count']}",
        reply_markup=IMAGE_COUNT_BUTTON,
        disable_web_page_preview=True,
    )


async def back2settings_callback(update, settings):
    await update.message.edit_text(
        text=f"""Current Settings:\n🤖 Model: {settings['model']}\n🚶‍♂️ Steps: {settings['steps']}\n
        🌱 Seed: {settings['seed']} \n🖼️ Image Count: {settings['image_count']}""",
        reply_markup=SETTINGS,
        disable_web_page_preview=True,
    )


async def start_callback(update):
    await update.message.edit_text(
        text=START_STRING.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTON,
    )
