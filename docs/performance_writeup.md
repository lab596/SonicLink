# Performance Tuning

## Distribution of Data

Data we added

View `src/fakestuff.py`

* 5k new users
* 500K user tags
* 1M user upvotes
* 3k challenges
* 3k challenge submissions

We believe this is a decent base to start stress testing our endpoints since it provides a good distribution of realistic database inserts. This is because our database is mostly tag focused so we expect a large amount of our user interactions to be tag focused interaction with a lot of upvotes per tag, thus a majority of our fake data is tags and their upvotes. Thus this will enable us to test a lot of our key functionality including `/leaderboard` - a sorting algo that will rank tag upvotes as well as `/weekly` - an algorithm that provides challenges made within the last week. 