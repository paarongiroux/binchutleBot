import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler
from diffusers.pipelines.stable_diffusion.convert_from_ckpt import download_from_original_stable_diffusion_ckpt
from pathlib import Path
import requests

class ImageGenerator:
    ckpt_url = "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt"
    ckpt_path = Path("sd-v1-4.ckpt")

    def __init__(self):
        if not self.ckpt_path.exists():
            print("Downloading sd-v1-4.ckpt...")
            with requests.get(self.ckpt_url, stream=True) as r:
                r.raise_for_status()
                with open(self.ckpt_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("Download complete.")


        self.checkpoint = torch.load(self.ckpt_path, map_location="cpu", weights_only=False)
        self.pipe = download_from_original_stable_diffusion_ckpt(
            self.checkpoint,
            original_config_file=None,
            from_safetensors=False,
            device="cpu",
        )

        self.pipe.scheduler = DDIMScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.save_pretrained("sd-v1-4-diffusers")

        self.pipe = StableDiffusionPipeline.from_pretrained(
            "sd-v1-4-diffusers",
            torch_dtype=torch.float32
        ).to("mps")

    def generate(self, prompt, path):
        image = self.pipe(
            prompt=prompt,
            num_inference_steps=10,
            guidance_scale=7.5,
            height=512,
            width=512,
        ).images[0]
        image.save(path)
