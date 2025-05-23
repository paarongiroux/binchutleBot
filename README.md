# BinchutleBot
Python script to generate an image based on an AI prompt and post it to instagram.

### `post_binchutle.py`
 - loads the llm and stable diffuse models, generates image and posts to instagram
 - Also uploads to S3 bucket and stores prompt / caption / URL in `image_log.csv`
 - requires instagram / AWS credentials to be set in .env file
 - requires huggingface-cli to be configured in order to download the models

### `llama.py`
  - uses [TinyLlama-1.1B-Chat-v1.0](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) to generate the prompt

### `image_gen.py` 
  - uses [stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4) to generate an image based on prompt from `llama.py`.

### `instagram_poster.py` 
  - use selenium to log into instagram and make a post.
  - instagram APIs are a pain to get access to, so I did this instead.

### `aws_uploader.py`
  - upload the file to my s3 bucket

### `csv_logger.py`
  - save the prompt, caption and s3 url into `image_log.csv`

# Example output:
<img src="https://binchutlebot.s3.us-east-2.amazonaws.com/output-20250522-082309.png" alt="carrot man example"/>

__prompt__: A man with a pet beetle tries to catch a fish with a fishhook made from a carrot, but it keeps slipping out.

__caption__: The man with the beetle hook tries to catch a fish with a fishhook made from a carrot, but it keeps slipping out.

checkout out the instagram account here: [https://www.instagram.com/binchutle/](https://www.instagram.com/binchutle/)
