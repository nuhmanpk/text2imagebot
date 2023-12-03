from dotenv import load_dotenv
import os

load_dotenv()

models = os.getenv("MODELS")

MODELS = [
    "prompthero/openjourney",
    "runwayml/stable-diffusion-v1-5",
    "CompVis/stable-diffusion-v1-4",
    "WarriorMama777/OrangeMixs",
    "stabilityai/stable-diffusion-2-1",
    "CompVis/stable-diffusion-v-1-4-original",
    "hakurei/waifu-diffusion",
    "stabilityai/stable-diffusion-2",
    "dreamlike-art/dreamlike-photoreal-2.0",
    "gsdf/Counterfeit-V2.5",
    "Yntec/AbsoluteReality",
    "digiplay/AbsoluteReality_v1.8.1",
    "Yntec/AbsoluteRemix",
    "Yntec/epiCPhotoGasm",
    "Yntec/Dreamshaper8",
    "Yntec/photoMovieRealistic",
    "Yntec/edgeOfRealism",
    "segmind/SSD-1B",
    "digiplay/Juggernaut_final",
    "stabilityai/stable-diffusion-xl-base-1.0",
]

if models:
    models_list = models.split(",")
    MODELS.extend(models_list)
