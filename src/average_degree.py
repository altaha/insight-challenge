import getopt
import sys

from tweeter import TweetGraphDegree, TweetSanitizer


## Feature 2 execution script ##
degrees_out = None

def write_line(line):
    degrees_out.write(line + '\n')

def calculate_all_tweets(input_file):
    sanitizer = TweetSanitizer()
    graph = TweetGraphDegree()
    with open(input_file) as tweets_in:
        for line in tweets_in:
            tweet = sanitizer.sanitize_tweet(line)
            graph.add_tweet(tweet)
            degree = graph.average_degree()
            write_line('{:0.2f}'.format(degree))


def main(argv):
    input_file = '../data-gen/tweets.txt'
    output_file = '../tweet_output/ft2.txt'
    try:
        (opts, args) = getopt.getopt(argv, 'i:o:')
    except getopt.GetoptError:
        print 'average_degree.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i'):
            input_file = arg
        elif opt in ('-o'):
            output_file = arg

    global degrees_out
    degrees_out = open(output_file, 'w')
    calculate_all_tweets(input_file)
    degrees_out.close()

if __name__ == '__main__':
    main(sys.argv[1:])
