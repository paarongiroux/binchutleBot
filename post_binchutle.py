from llama import LlamaModel
from imageGen import ImageGenerator
from instagram_poster import makeInstagramPost
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")


llmModel = LlamaModel()
prompt, caption = llmModel.getImagePrompt()

generator = ImageGenerator()
outputFile = "output.png"
generator.generate(prompt, outputFile)


script_dir = Path(__file__).parent.resolve()
image_path = script_dir / outputFile


print("\n\nSUMMARY==================")
print(" - PROMPT: ", prompt)
print(" - CAPTION:", caption)
print(" - IMAGE:  ", image_path)

makeInstagramPost(username, password, image_path, caption)