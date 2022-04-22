import create_query as create_query
import retriever as retriever
import database
import sys

from datetime import datetime


def main():
    arg_length = len(sys.argv)
    db = database.Connection()

    if arg_length < 2:
        print(
            "\nflags:" "\n\t--create-json: creates table json files",
            "\n\t--init-insert: executes initial data insertion",
            "\n\t--create-tables: creating tables"
            "\n\t--delete-tables: deletes all tables in database",
            "\n\t--patch: apply a patch",
            "\n\t--debug: utilized for development",
        )

    else:
        for i in range(1, arg_length):
            arg = sys.argv[i]

            if arg == "--create-json":
                print("\n--init-insert: creating json")
                create_query.export_all()

            elif arg == "--init-insert":
                print("\n--init-insert: carrying out initial insertion")
                reddit = retriever.Reddit()

                # retrieving posts from reddit, and columns list from db
                after = int(datetime(2021, 9, 20).timestamp())  # past 6 months
                for subreddit in retriever.SUBREDDITS:
                    posts = reddit.posts__from_subreddit(subreddit, after)

                    # inserting posts
                    for i, post in enumerate(posts):
                        db.insert_row("unannotated_posts", post)

            elif arg == "--create-tables":
                print("\n--create-tables: creating tables")
                for table in database.TABLES:
                    db.create_table(table)

            elif arg == "--drop-tables":
                print("\n--delete-tables: deleting tables")
                for table in create_query.TABLES:
                    db.drop_table(table)

            elif arg == "--patch":
                print("\n--patch: apply a patch")
                print("No patch implemented")

            elif arg == "--debug":
                print("\n--debug: debugging implementation")
                create_query.export_all()

                db.drop_table("unannotated_posts")
                db.create_table("unannotated_posts")
                reddit = retriever.Reddit()

                # retrieving posts from reddit, and columns list from db
                after = int(datetime(2022, 4, 22).timestamp())  # since start of today
                posts = reddit.posts__from_subreddit("stocks", after)

                # inserting posts
                for i, post in enumerate(posts):
                    print(f"\n{i}.\nTickers: {post[8]}\nLink: {post[18]}")
                    db.insert_row("unannotated_posts", post)


if __name__ == "__main__":
    main()
