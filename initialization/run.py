import sys
import initial_insertion
import delete_table
import create_table_json


def main():
    arg_length = len(sys.argv)

    if arg_length < 2:
        print(
            "--create-json: creates table json files",
            "--init-insert: executes initial data insertion\n",
            "--delete-tables: deletes all tables in database\n",
        )

    else:
        for i in range(1, arg_length):
            arg = sys.argv[i]

            if arg == "--create-json":
                print("--init-insert: creating json")
                create_table_json.create_save_folder_if_not_exist()
                create_table_json.unannotated_posts()

            elif arg == "--init-insert":
                print("--init-insert: carrying out initial insertion")
                initial_insertion.unannotated_posts()

            elif arg == "--delete-tables":
                print("--delete-tables: deleting tables")
                delete_table.unannotated_posts()


if __name__ == "__main__":
    main()
