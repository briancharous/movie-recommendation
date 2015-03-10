from __future__ import division
from RecommendationBase import User
from RecommendationBase import Movie
import RecommendationBase as base
import csv
import argparse

def similarity_between_items(training_filename):
    matrix = base.matrix_from_filename(training_filename)
    users = base.ratings_by_user(matrix)
    movie_ratings = base.ratings_by_movie(users)

    movie_ids = movie_ratings.keys()
    all_distances = {}
    for i in range(0, len(movie_ids)):
        movie_1_id = movie_ids[i]
        movie_1 = movie_ratings[movie_1_id]
        distances = []
        for j in range(i, len(movie_ids)):
            movie_2_id = movie_ids[j]
            movie_2 = movie_ratings[movie_2_id]
            # print movie_1.users, movie_2.users
            dist = base.cosine_distance_items(movie_1, movie_2)
            distances.append((dist, movie_2_id))
        all_distances[movie_1_id] = sorted(distances)
    return all_distances, users

def predict_rating(user, distances):
    rating = 0
    k = 5 # magic number
    closest_movies = distances[0:k]
    print "length: {}".format(len(closest_movies))
    rating_sum = 0
    for item in closest_movies:
        movie_id = item[1]
        rating_sum += user.mean + user.ratings[movie_id]
    return rating_sum/k

def recommend(training_filename, test_filename):
    all_distances, users = similarity_between_items(training_filename)
    with open(test_filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            user_id = int(row[0])
            movie_id = int(row[1])
            actual_rating = int(row[2])
            predicted_rating = predicted_rating(users[user_id], all_distances[movie_id])
            print "user: {0}, movie: {1}, actual: {2}, predicted: {3}".format(user_id, 
                                                                        movie_id, actual_rating, 
                                                                        predicted_rating)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=True, help='Filename for training set')
    parser.add_argument('-te', '--test', required=True, help="Filename for test set")
    args = parser.parse_args()

    recommend(args.training, args.test)

if __name__ == '__main__':
    main()