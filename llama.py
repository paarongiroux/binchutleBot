import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

messages = [
    {"role": "system", "content": (
        "You're an assistant that generates only short, vivid prompts for an image generator. "
        "The prompt should be funny, weird, and surprising. Most importantly, it should be simple"
        "Keep it under 20 words. Do not add explanations or commentary. Just the prompt. If the user asks for a caption, provide one for the last image description"
    )},
    {"role": "user", "content": "Give me a prompt."},
    {"role": "assistant", "content": "A giant cat wearing sunglasses lounges on a floating island made of rainbow pancakes."},
    {"role": "user", "content": "Give me a caption for that."},
    {"role": "assistant", "content": "Sunglasses cat chilling"},
    {"role": "user", "content": "Give me another prompt."},
    {"role": "assistant", "content": "A vintage typewriter grows flowers instead of letters, blooming in a desert of pastel clouds."},
    {"role": "user", "content": "Give me a caption for that."},
    {"role": "assistant", "content": "Typing is the flowers of the soul."},
    {"role": "user", "content": "Give me one more prompt"},
    {"role": "assistant", "content": "A squirrel in a tuxedo DJ spins records on giant acorns at a woodland dance party."},
    {"role": "user", "content": "Give me a caption for that."},
    {"role": "assistant", "content": "DJ Tuxedo Nut live in the woods."},
    {"role": "user", "content":"give me another prompt"}
]

prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

inputs = tokenizer(prompt, return_tensors="pt").to(device)

streamer = TextStreamer(tokenizer)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        # streamer=streamer,
        do_sample=True,
        temperature=0.7,
        top_p=0.95
    )

decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Split based on the <|assistant|> tag
parts = decoded.split("<|assistant|>")

# The last non-empty string after the last <|assistant|> should be the model's final response
image_prompt = parts[-1].strip()

print("Prompt:", image_prompt)

messages.append({"role": "assistant", "content": image_prompt})
messages.append({"role": "user", "content": "Give me a caption for that."})

caption_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
caption_inputs = tokenizer(caption_prompt, return_tensors="pt").to(device)

with torch.no_grad():
    caption_outputs = model.generate(
        **caption_inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7,
        top_p=0.95
    )

caption_decoded = tokenizer.decode(caption_outputs[0], skip_special_tokens=True)
caption = caption_decoded.split("<|assistant|>")[-1].strip()
print("Caption:", caption)