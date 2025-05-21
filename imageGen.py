import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler
from diffusers.pipelines.stable_diffusion.convert_from_ckpt import download_from_original_stable_diffusion_ckpt
from pathlib import Path
import requests
import argparse

parser = argparse.ArgumentParser(description="Generate an image from a prompt using Stable Diffusion.")
parser.add_argument("--prompt", type=str, required=True, help="Text prompt for image generation.")
args = parser.parse_args()
prompt = args.prompt

# Download .ckpt if needed
ckpt_url = "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt"
ckpt_path = Path("sd-v1-4.ckpt")

if not ckpt_path.exists():
    print("Downloading sd-v1-4.ckpt...")
    with requests.get(ckpt_url, stream=True) as r:
        r.raise_for_status()
        with open(ckpt_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print("Download complete.")


print("Loading checkpoint...")
checkpoint = torch.load(ckpt_path, map_location="cpu", weights_only=False)

# Convert ckpt to diffusers pipeline
print("Converting .ckpt to diffusers pipeline...")
pipe = download_from_original_stable_diffusion_ckpt(
    checkpoint,
    original_config_file=None,
    from_safetensors=False,
    device="cpu",
)

# Use DDIM scheduler to match Tinygrad-style setup
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

# Save locally
pipe.save_pretrained("sd-v1-4-diffusers")

# Load and move to GPU
pipe = StableDiffusionPipeline.from_pretrained(
    "sd-v1-4-diffusers",
    torch_dtype=torch.float32
).to("mps")

# Prompt + generation (no seed)
image = pipe(
    prompt=prompt,
    num_inference_steps=10,
    guidance_scale=7.5,
    height=512,
    width=512,
).images[0]

# Save output
image.save("output.png")
print("Saved image to output.png")