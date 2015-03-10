from __future__ import division
import argparse
import csv
import numpy as np
import math

class User(object):
    """ simple wrapper class """

    def normalize_ratings(self):
        """ normalize ratings for user """
        ratings = self.ratings.values()
        mean = np.mean(ratings)
        for mid in self.ratings:
            self.ratings[mid] = self.ratings[mid] - mean

    def __init__(self):
        super(User, self).__init__()
        self.ratings = {}

class Movie(object):
    """ simple wrapper class for movie"""

    def __init__(self):
        super(Movie, self).__init__()
        self.users = {}

def matrix_from_filename(filename):
    """ get the data. nothing to special happening here """
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            rows.append([int(r) for r in row[:-1]])
    return rows

def ratings_by_user(matrix):
    """ returns a dictionary of user objects with their ratings for each movie filled in """
    users = {}
    for row in matrix:
        user_id = row[0]
        movie_id = row[1]
        rating = row[2]
        user = None
        if user_id in users:
            user = users[user_id]
        else:
            user = User()
            users[user_id] = user
        user.ratings[movie_id] = rating
    for uid in users:
        users[uid].normalize_ratings()
    return users

def ratings_by_movie(users):
    """ returns a dictionary of users who have rated each movie by id. take in a list of users 
    (i.e. generated in ratings_by_user) so that the ratings have been normalized """
    movies = {}
    for uid in users.keys():
        for movie_id in users[uid].ratings:
            rating = users[uid].ratings[movie_id]
            movie = None
            if movie_id in movies:
                movie = movies[movie_id]
            else:
                movie = Movie()
                movies[movie_id] = movie
            movie.users[uid] = rating
    return movies


def cosine_distance(user1, user2):
    """ cosine distance between 2 users """
    both_rated = set(user1.ratings.keys()) & set(user2.ratings.keys())
    numerator = 0
    for movie_id in both_rated:
        u1rating = user1.ratings[movie_id]
        u2rating = user2.ratings[movie_id]
        numerator += u1rating * u2rating
    u1magnitude = math.sqrt(reduce(lambda x, y: x+y**2, user1.ratings.values()))
    u2magnitude = math.sqrt(reduce(lambda x, y: x+y**2, user2.ratings.values()))
    denominator = u1magnitude + u2magnitude
    return numerator/denominator

def cosine_distance_items(movie1, movie2):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=False, help='Filename for training set')
    args = parser.parse_args()

    ratings_by_user(matrix_from_filename(args.training))

if __name__ == '__main__':
    main()