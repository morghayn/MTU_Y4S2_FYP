from transformers import GPT2TokenizerFast
from warnings import resetwarnings
import database
import openai
import os
import re
import time

from dotenv import load_dotenv

load_dotenv()
db = database.Connection()
openai.api_key = os.getenv("OPENAI_KEY")

ENGINE = "text-babbage-001"
ANNOTATOR_USERNAME = f"gpt-3-{ENGINE}"
ANNOTATOR_ID = 1

SENTIMENT_MAP = {"positive": 1, "neutral": 0, "negative": -1}

annotator_id = ANNOTATOR_ID  # db.get_annotator_id(ANNOTATOR_USERNAME)


def send_random_request(misses):
    post = db.select_random_unannotated_post(ANNOTATOR_USERNAME)
    post_id = post["id"]
    prompt = f"Classify sentiment of post as either positive, neutral or negative:\n\n\nTitle:\n{post['title']}\nText:\n{post['text']}\n\nSentiment:"
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    tokens = (len(tokenizer(prompt)['input_ids']) + 16)

    if tokens < 2049:
        print(f"\nPost ID: {post_id}\nToken Count: {tokens}")
        response = openai.Completion.create(
            engine=ENGINE,
            prompt=prompt,
            temperature=0,
            max_tokens=None,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        annotation = response["choices"][0]["text"]
        timestamp = response["created"]
        res = re.sub("\s+", "", annotation).lower()
        if res in SENTIMENT_MAP:
            sentiment = SENTIMENT_MAP[res]

            print(f"Sentiment: {sentiment}\nTimestamp: {timestamp}")
            db.insert(
                "annotations",
                [post_id, annotator_id, sentiment, timestamp],
                auto_increment=True,
                notify=True,
            )
            return 1
        else:
            return 2
    return 3


misses = 0
bad_response = 0
for i in range(0, 10000):
    res = send_random_request(misses)
    if res is 1:
        time.sleep(1)
    elif res == 2:
        bad_response += 1
    elif res == 3:
        misses += 1
        print(misses)
    
    if bad_response > 5:
        break;
