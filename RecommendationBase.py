import argparse
import csv

class User(object):
    """ simple wrapper class """
    def insert_rating(movie_id, rating):
        self.ratings[movie_id] = rating

    def has_rated_movie(movie_id):
        return movie_id in self.ratings

    def __init__(self):
        super(User, self).__init__()
        self.ratings = {}


def matrix_from_filename(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            rows.append(row[:-1])
            print row[:-1]
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=False, help='Filename for training set')
    args = parser.parse_args()

    matrix_from_filename(args.training)

if __name__ == '__main__':
    main()