# Algorithms

This folder will house the projects files that will be used to assist in achieving the algorithm research this project has stated it would carry out.

The algorithms which we will be researching are as follows..
1. VADER
2. Naïve Bayes
3. Support-Vector Machines
4. Long Short-Term Memory
5. Convolutional Neural Network
6. BERT (Additional Research)

We will be comparing and figuring out the best fit algorithm to deploy for automatically determining the sentiment of Reddit posts using

# Dataset
Not every column retrieved and stored in our database will be selected for our dataset. Rather, the most useful from a training perspective will be selected. All personal identifying information will be dropped, aside from the post id. The columns selected may change at a further date under future work.

| Column | Description |
| --- | --- |
| id | ID of the post |
| creation_time_utc | Time post was created |
| subreddit_display_name | Subreddit name |
| title | Post title |
| text | Post body |
| score | Amount of upvotes |
| num_of_comments | Number of comments |
| ticker_list | Tickers mentioned in post |
| sentiment | Sentiment rating |
