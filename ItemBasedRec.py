from RecommendationBase import User
from RecommendationBase import Movie
import RecommendationBase as base

def similarity_between_items(training_filename):
    matrix = base.matrix_from_filename(training_filename)
    user_ratings = base.ratings_by_user(matrix)
    movie_ratings = base.ratings_by_movie(user_ratings)
    movie_ids = movie_ratings.keys()
    for i in range(0, len(movie_ids)):
        movie_id_1 = movie_ids[i]
        movie_ratings_1 = movie_ratings[movie_id_1]
        for j in range(i, len(movie_ids)):
            movie_id_2 = movie_ids[j]
            movie_ratings_2 = movie_ratings[movie_id_2]



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=True, help='Filename for training set')
    parser.add_argument('-te', '--test', re)
    args = parser.parse_args()

if __name__ == '__main__':
    main()