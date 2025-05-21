# so this is going to be the main file.

# download weights for llm and stablediffusion
# instantiate LLM object
# instantiate imageGen object

# LLM.getInstagramPost --> returns a tuple with 0=prompt, 1=caption
# imageGen.createImage --> puts an image in output.png -- maybe add a timestamp to the filename

# then need to use GraphAPI to make an instagram post.
# my understanding is that this works like so:
    # 1. upload the image to meta storage API. could also add to S3.. the point is that I need an image URL for the posting API
        # the meta image API actually includes caption which will be used in the post so that is likely the better option
    # 2. call the API to make an image post, supplying the image URL.
# ^ this will require me to have a business or creator account on instagram. -- will need to make a corresponding facebook


#OPENCOURSE - app idea where students can post unfinished homework assignments and projects as well as reading assignments / topics of each lecture
from llama import LlamaModel
from imageGen import ImageGenerator

llmModel = LlamaModel()
prompt, caption = llmModel.getImagePrompt()

generator = ImageGenerator()
path = "output.png"
generator.generate(prompt, path)

print("\n\nSUMMARY==================")
print(" - PROMPT: ", prompt)
print(" - CAPTION:", caption)
print(" - IMAGE:  ", path)