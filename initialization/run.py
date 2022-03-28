import sys
import initial_insertion
import delete_table


def main():
    arg_length = len(sys.argv)

    if arg_length < 2:
        print("--init: initialize insertion\n", "--del: delete unannotated post table\n")

    else:
        for i in range (1, arg_length):
            arg = sys.argv[i]

            if arg == "--init":
                initial_insertion.unannotated_posts()
            elif arg == "--del":
                delete_table.unannotated_posts()


if __name__ == "__main__":
    main()
