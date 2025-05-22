from llama import LlamaModel
from imageGen import ImageGenerator
from aws_uploader import BucketUploader
from csv_logger import log_image_to_csv
from instagram_poster import makeInstagramPost
from dotenv import load_dotenv
import os
from pathlib import Path
from datetime import datetime

load_dotenv()
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_REGION", "us-west-2")


timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
outputFile = f"outputs/output-{timestamp}.png"

llmModel = LlamaModel()
print("Generating image prompt...")
prompt, caption = llmModel.getImagePrompt()

generator = ImageGenerator()
print("Generating image...")
generator.generate(prompt, outputFile)

script_dir = Path(__file__).parent.resolve()
image_path = script_dir / outputFile

bucketUploader = BucketUploader("binchutlebot", access_key, secret_key, region)
print("Uploading to S3 bucket...")
s3_url = bucketUploader.upload_image(outputFile)

print("\n\nSUMMARY==================")
print(" - PROMPT: ", prompt)
print(" - CAPTION:", caption)
print(" - IMAGE:  ", image_path)
print(" - URL:    ", s3_url)

log_image_to_csv(prompt, caption, s3_url)
print("\nPosting to instagram...")
makeInstagramPost(username, password, str(image_path), caption)