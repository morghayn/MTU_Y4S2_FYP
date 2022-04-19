import sys

import create_query as create_query
import database
import retriever


def main():
    arg_length = len(sys.argv)
    db = database.Connection()

    if arg_length < 2:
        print(
            "--create-json: creates table json files",
            "--init-insert: executes initial data insertion\n",
            "--delete-tables: deletes all tables in database\n",
            "--debug: utilized for development\n",
        )

    else:
        for i in range(1, arg_length):
            arg = sys.argv[i]

            if arg == "--create-json":
                print("--init-insert: creating json")
                create_query.export_all()

            elif arg == "--init-insert":
                print("--init-insert: carrying out initial insertion")
                # TODO

            elif arg == "--drop-tables":
                print("--delete-tables: deleting tables")
                for table in create_query.TABLES:
                    db.drop_table(table)

            elif arg == "--debug":
                print("--debug: debugging implementation")
                create_query.export_all()

                db.drop_table("unannotated_posts")
                db.create_table("unannotated_posts")
                reddit = retriever.Reddit()
                
                # retrieving posts from reddit, and columns list from db
                posts = reddit.posts__from_subreddit__since__limited_to("Stocks", "month", 10)
                columns = db.get_columns_list("unannotated_posts")

                # inserting posts
                for i, post in enumerate(posts):
                    print(f"\n{i}.\nTickers: {post[8]}\nLink: https://reddit.com/r/stocks/comments/{post[4]}")
                    res = db.insert_row("unannotated_posts", post)
                    if res == False:
                        print("I crashed")
                        break

            


if __name__ == "__main__":
    main()
