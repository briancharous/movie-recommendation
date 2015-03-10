from __future__ import division
from RecommendationBase import User
from RecommendationBase import Movie
import RecommendationBase as base
import csv
import argparse
import math
import operator

def similarity_between_items(training_filename):
    """ calculate distance between every pairing of ratings. return 
    both the users list and a dictionary whose key is a movie id and whose
    value is a sorted list of the distance to every other movie object
    (that appears after it when listed by id #) """
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
            dist = base.cosine_distance_items(movie_1, movie_2)
            distances.append((dist, movie_2_id))
        all_distances[movie_1_id] = sorted(distances)
    return all_distances, users

def predict_rating(user, distances, uid, movie_id):
    """ predicts rating for a given user and given movie 
    by finding the items a user has already rated most similar to 
    the item in question """
    rating = 0
    k = 4 # magic number, seems to give the lowest RMSE
    cur_k = 0
    rating_sum = 0
    for item in distances:
        movie_id = item[1]
        if user.has_rated_movie(movie_id):
            rating_sum += user.mean + user.ratings[movie_id]
            cur_k += 1
        if cur_k == k:
            break
    # if cur_k < k:
    #     print "WARNING: Possibly insufficient data to predict movie {0} for user {1}".format(uid, movie_id)
    return int(round(rating_sum/k))

def recommend(training_filename, test_filename):
    print "Computing item similarities..."
    all_distances, users = similarity_between_items(training_filename)
    print "I will now consult my crystal ball and make predictions..."
    error = 0
    recs_made = 0
    error_by_movie = {}
    occurrences_of_movie = {}
    with open(test_filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            user_id = int(row[0])
            movie_id = int(row[1])
            actual_rating = int(row[2])
            if movie_id in all_distances and user_id in users:
                predicted_rating = predict_rating(users[user_id], all_distances[movie_id], user_id, movie_id)
                # print "user: {0}, movie: {1}, actual: {2}, predicted: {3}".format(user_id, 
                #                                                             movie_id, actual_rating, 
                #                                                             predicted_rating)

                # keep track of total error
                error += (actual_rating - predicted_rating)**2
                recs_made += 1

                # keep track of error by movie
                if movie_id not in error_by_movie:
                    error_by_movie[movie_id] = 0
                error_by_movie[movie_id] += (actual_rating - predicted_rating)**2

                # keep track of # of times we've seen each movie
                if movie_id not in occurrences_of_movie:
                    occurrences_of_movie[movie_id] = 0
                occurrences_of_movie[movie_id] += 1

    # calculate error for each movie
    for movie in error_by_movie:
        occurrences = occurrences_of_movie[movie]
        error_by_movie[movie] = math.sqrt(error_by_movie[movie]/occurrences)

    sorted_by_error = sorted(error_by_movie.items(), key=operator.itemgetter(1))
    print "Best predicted movies:"
    for best in sorted_by_error[:10]:
        print best[0]
    print
    print "Worst predicted movies:"
    for worst in sorted_by_error[-10:]:
        print worst[0]
    print

    rmse = math.sqrt(error/recs_made)
    print "Total RMSE: {0}".format(rmse)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=True, help='Filename for training set')
    parser.add_argument('-te', '--test', required=True, help="Filename for test set")
    args = parser.parse_args()

    recommend(args.training, args.test)

if __name__ == '__main__':
    main()