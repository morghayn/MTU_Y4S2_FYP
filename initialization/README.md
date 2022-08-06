# About
All files in this folder are intended to assist in the initiliazation of our database. Every file within this folder of the project has been developed so as to support future work. 

i.e.,: 
1. [database.py](/initialization/database.py) has been written to accept generic inputs. Nothing is hardcoded and we should be able to add as many new MySQL (MariaDB in our case) tables with ease. 
2. [create_table_json.py](/initialization/create_table_json.py) allows us to write out our SQL tables as dictionaries and export them in JSON format for later parsing. This is purely due to personal preference/opinion, but dictionaries/JSON is a very readable and maintainble format to write SQL.

# Dataset Range
|Entry|Date|
|---|---|
|Dataset Start|Tue Jan 01 2019 00:31:03 GMT+0000|
|Blackout Period #1 - Start|Wed Jan 20 2021 00:00:00 GMT+0000|
|Blackout Period #1 - End|Sat Jan 30 2021 11:59:59 GMT+0000|
|Dataset End|Mon Apr 25 2022 13:25:02 GMT+0000|

The cause for the first blackout period was due to a huge spike of posts (100,000 posts per day) on Wallstreet bets in and around the 25th of January 2021.

# Notes
## What is the "initial insertion"?
The initial insertion is whereby we fetch posts from the past year that meet the criteria we defined, a post/comment mentioning a company's name or stock ticker that is enlisted within the S&P500 index.

Further, this list may be extended at some point to allow for other stocks of our choosing to be included. The reason we have opted for such a means of post/comment selection is so as not to retrieve posts mentioning companies with very low market caps, as this will retrieve low-quality "pumper-posts".

Is this making our data biased? Perhaps. But we can deduce we will be retrieving higher quality data, and the intentions of this dataset is to applied only to stable-medium risk financial securities; i.e, mid-cap stocks (market caps with $2-10 billion) and large-cap stocks.

## Dangers of the delete table command.
The delete table command is dangerous and is recognized as such. Measures to prevent accidental deletion will be implemented as this project progresses.

## Column retrieval of database.py
Database.py knows the column names of each table by reading the raw create table query. Without this, database.py will not know of the column names of a table as we do not fetch this data from SQL through a query (obviously).