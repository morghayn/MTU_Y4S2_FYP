from algorithm import bayes, bert, cnn, lstm, svm, vader
import database
import sys

DATASET_COLUMNS = [
    "up.id",
    "up.creation_time_utc",
    "up.subreddit_display_name",
    "up.title",
    "up.text",
    "up.score",
    "up.num_of_comments",
    "up.ticker_list",
    "a.sentiment",
]
# up = unannotated_posts
# a = annotations


def main():
    arg_length = len(sys.argv)
    db = database.Connection()

    if arg_length < 2:
        print(
            "\nflags:",
            "\n\t--compile: compiles dataset",
            "\n\t--vader: VADER algorithm analysis",
            "\n\t--bayes: Naïve Bayes algorithm analysis"
            "\n\t--svm: Support-Vector Machines algorithm analysis",
            "\n\t--lstm: Long Short-Term Memory algorithm analysis",
            "\n\t--cnn: Convolutional Neural Network algorithm analysis",
            "\n\t--bert: BERT algorithm analysis",
            "\n\t--debug: utilized for development",
        )

    else:
        for i in range(1, arg_length):
            arg = sys.argv[i]

            if arg == "--vader":
                print()
                vader.run()
            elif arg == "--bayes":
                print()
                bayes.run()
            elif arg == "--svm":
                print()
                svm.run()
            elif arg == "--lstm":
                print()
                lstm.run()
            elif arg == "--cnn":
                print()
                cnn.run()
            elif arg == "--bert":
                print()
                bert.run()
            elif arg == "--debug":
                df = db.select__from__by__(DATASET_COLUMNS, "curie")
                print(df)


if __name__ == "__main__":
    main()
