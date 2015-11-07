import getopt
import sys

from tweeter import TweetSanitizer


## Feature 1 execution script ##
tweets_out = None

def write_line(line):
    tweets_out.write(line + '\n')

def sanitize_all_tweets(input_file):
    sanitizer = TweetSanitizer()
    with open(input_file) as tweets_in:
        for line in tweets_in:
            tweet = sanitizer.sanitize_tweet(line)
            write_line(str(tweet))

        write_line('')
        num_unicode = sanitizer.num_tweets_with_unicode()
        write_line('{0} tweets contained unicode.'.format(num_unicode))


def main(argv):
    input_file = '../data-gen/tweets.txt'
    output_file = '../tweet_output/ft1.txt'
    try:
        (opts, args) = getopt.getopt(argv, 'i:o:')
    except getopt.GetoptError:
        print 'sanitize_tweets.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i'):
            input_file = arg
        elif opt in ('-o'):
            output_file = arg

    global tweets_out
    tweets_out = open(output_file, 'w')
    sanitize_all_tweets(input_file)
    tweets_out.close()

if __name__ == '__main__':
    main(sys.argv[1:])
