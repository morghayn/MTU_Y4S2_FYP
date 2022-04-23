import database

db = database.Connection()
posts = db.select_50_random_posts()

for post in posts:
    print(post.title)
