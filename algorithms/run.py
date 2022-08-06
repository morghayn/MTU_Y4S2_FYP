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


def notify(algorithm):
    print(f"Starting {algorithm}.")


def main():
    arg_length = len(sys.argv)
    db = database.Connection()

    if arg_length < 2:
        print(
            "\nflags:",
            "\n\t--vader: VADER algorithm analysis",
            "\n\t--bayes: Naïve Bayes algorithm analysis"
            "\n\t--svm: Support-Vector Machines algorithm analysis",
            "\n\t--lstm: Long Short-Term Memory algorithm analysis",
            "\n\t--cnn: Convolutional Neural Network algorithm analysis",
            "\n\t--bert: BERT algorithm analysis",
            "\n\t--debug: utilized for development",
        )

    else:
        df = db.select_columns_annoatoted_by(DATASET_COLUMNS, "curie")
        # df.to_excel("reddit_data.xlsx", sheet_name='curie')

        for i in range(1, arg_length):
            arg = sys.argv[i]

            if arg == "--vader":
                notify("VADER")
                vader.run(df)
            elif arg == "--bayes":
                notify("Naive Bayes")
                bayes.run(df)
            elif arg == "--svm":
                notify("SVM")
                svm.run(df)
            elif arg == "--lstm":
                print("LSTM")
                lstm.run(df)
            elif arg == "--cnn":
                notify("CNN")
                cnn.run(df)
            elif arg == "--bert":
                notify("BERT")
                bert.run(df)
            elif arg == "--debug":
                notify("Debugging")


if __name__ == "__main__":
    main()
