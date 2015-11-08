#!/usr/bin/env bash

# I'll execute my programs, with the input directory tweet_input and output the files in the directory tweet_output
python ./src/sanitize_tweets.py -i ./tweet_input/tweets.txt -o ./tweet_output/ft1.txt
python ./src/average_degree.py -i ./tweet_input/tweets.txt -o ./tweet_output/ft2.txt

# The code assumes standard python 2.7 installation, and only imports standard python modules

