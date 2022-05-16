import database

from dotenv import load_dotenv
load_dotenv()
db = database.Connection()

ADA_COST = 0.0006
BABBAGE_COST = 0.0012
CURIE_COST = 0.0060
DAV_COST = 0.06

ENGINE = "text-babbage-001"
ANNOTATOR_USERNAME = f"gpt-3-{ENGINE}"

def print_cost(length, message):
    print(message)
    tokens = length * 0.75
    print(f"{length} characters")
    print(f"{tokens} tokens")
    print(f"Ada: ${(tokens/1000) * ADA_COST:.5f}")
    print(f"Babbage: ${(tokens/1000) * BABBAGE_COST:.5f}")
    print(f"Curie: ${(tokens/1000) * CURIE_COST:.5f}")
    print(f"DaVinci: ${(tokens/1000) * DAV_COST:.5f}")


# # Single Random Post Cost
# post = db.select_random_unannotated_post(ANNOTATOR_USERNAME, 20)
# prompt = "Classify sentiment of post as either positive, neutral or negative:\n\n"
# prompt += f"\nTitle:\n{post['title']}\nText:\n{post['text']}\n\n"
# prompt += "Sentiment:"
# print_cost(len(prompt), "\n\nSingle Random Post Total Cost")


# All Post Cost
# posts = db.select_all_posts()
# prompts = ""
# for post in posts:
#     prompts += "Classify sentiment of post as either positive, neutral or negative:\n\n"
#     prompts += f"\nTitle:\n{post['title']}\nText:\n{post['text']}\n\n"
#     prompts += "Sentiment:"
# print_cost(len(prompts), "\n\nAll Posts Total Cost")


# Posts greater than x upvotes
upvote_limit = 20
posts = db.select_all_posts__with_greater_than_x_upvotes(upvote_limit)
prompts = ""
for post in posts:
    prompts += "Classify sentiment of post as either positive, neutral or negative:\n\n"
    prompts += f"\nTitle:\n{post['title']}\nText:\n{post['text']}\n\n"
    prompts += "Sentiment:"
print_cost(
    len(prompts), f"\n\nAll Posts with more than {upvote_limit} Upvotes Total Cost"
)
