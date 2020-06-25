# Tweet-Sentiment-Analyzer

The python file is a program that creates a suffix array given a series of tweets in a CSV file. The specifics of which are detailed in comments in the file. The algorithm to create the suffix array is prefix doubling from Manber-Myers. The suffix array allows for constant time lookups for words in all the tweets, allowing for easy sentiment analysis. The CSV which the py file is formatted to work with is from https://www.kaggle.com/kazanova/sentiment140
