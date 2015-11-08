#!/usr/bin/env bash

# run script for running tests

python -m unittest src.test_sanitize_tweets
python -m unittest src.test_average_degree

