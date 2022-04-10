import sys

import create_table_json
import database

TABLES = ["unannotated_posts"]


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
                create_table_json.create_save_folder_if_not_exist()
                for table in TABLES:
                    create_table_json.export(table)

            elif arg == "--init-insert":
                print("--init-insert: carrying out initial insertion")
                # TODO

            elif arg == "--drop-tables":
                print("--delete-tables: deleting tables")
                for table in TABLES:
                    db.drop_table(table)

            elif arg == "--debug":
                print("--debug: debugging implementation")
                # DEBUG


if __name__ == "__main__":
    main()
