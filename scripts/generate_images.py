"""
Allows you to *generate* images using the OpenAI image generation API.
"""

import io
import json
import os
import re
import traceback

import openai
import PIL.Image
import concurrent.futures
import requests

oai = openai.OpenAI()

import pandas as pd


def generate_image(query_english, query_korean, out_folder: str) -> str:
    try:
        print("generating:", query_english)

        data = json.loads(
            oai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You generate prompts for image generation models. Your goal is to generate images that would be useful as cues for practicing language learning. Make your prompts concise and not overly complicated. Find a simple way to clearly / distinctly represent the concept. Do not include any words in the image itself.",
                    },
                    {
                        "role": "user",
                        "content": f"Please generate a detailed prompt for the query: {query_english} ({query_korean})",
                    },
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "generate_prompt",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "step_by_step_reasoning": {"type": "string"},
                                "prompt": {"type": "string"},
                            },
                            "additionalProperties": False,
                            "required": ["step_by_step_reasoning", "prompt"],
                        },
                        "strict": True,
                    },
                },
            )
            .choices[0]
            .message.content  # type: ignore
        )

        print(data["step_by_step_reasoning"])
        print(data["prompt"])

        response = oai.images.generate(
            model="dall-e-3",
            prompt=data["prompt"],
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url",
        )
        image_url = response.data[0].url

        image_content = requests.get(image_url).content

        out_path = out_folder + "/" + re.sub("[^a-zA-Z,]", "_", query_english) + ".png"

        image = PIL.Image.open(io.BytesIO(image_content))

        image.save(out_path)

        return out_path
    except Exception as e:
        traceback.print_exc()
        raise


df = pd.read_csv("../decks/week002_deck.csv")
out_folder = "../media/images/week002"
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

images = []
jobs = []

with concurrent.futures.ThreadPoolExecutor(1) as exec:
    job = lambda query_english, query_korean: generate_image(
        query_english, query_korean, out_folder
    )
    images = exec.map(job, df["English Word"], df["한국어 단어"])

df["Image"] = images
df.to_csv("week002_deck_with_images.csv")
