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
            "\n\t--insert: executes data insertion",
            "\n\t--create-tables: creating tables"
            "\n\t--delete-tables: deletes all tables in database",
            "\n\t--patch: apply a patch",
            "\n\t--debug: utilized for development",
        )

    else:
        for i in range(1, arg_length):
            arg = sys.argv[i]

            if arg == "--create-json":
                print("\n--insert: creating json")
                create_query.export_all()

            elif arg == "--insert":
                print("\n--insert: carrying out initial insertion")
                reddit = retriever.Reddit()

                # retrieving posts from reddit, and columns list from db
                after = int(datetime(2021, 9, 20).timestamp())  # past 6 months
                for subreddit in retriever.SUBREDDITS:
                    posts = reddit.posts__from_subreddit(subreddit, after)

                    # inserting posts
                    print(f"\nFinished processing records for r/{subreddit}.")
                    print("Will now insert processed records.")
                    for i, post in enumerate(posts):
                        db.insert_row("unannotated_posts", post)

            elif arg == "--create-tables":
                print("\n--create-tables: creating tables")
                for table in database.TABLES:
                    db.create_table(table)

            elif arg == "--drop-tables":
                print("\n--delete-tables: deleting tables")
                for table in create_query.TABLES:
                    # db.drop_table(table)
                    pass

            elif arg == "--patch":
                print("\n--patch: apply a patch")
                print("No patch implemented")

            elif arg == "--debug":
                print("\n--debug: debugging insertion")
                reddit = retriever.Reddit()

                # retrieving posts from reddit, and columns list from db
                after = int(datetime(2022, 4, 20).timestamp())  # past 6 months
                for subreddit in retriever.SUBREDDITS:
                    posts = reddit.posts__from_subreddit(subreddit, after)

                    # inserting posts
                    print(f"\nFinished processing records for r/{subreddit}.")
                    print("Will now insert processed records.")
                    for i, post in enumerate(posts):
                        db.insert_row("unannotated_posts", post)


if __name__ == "__main__":
    main()
