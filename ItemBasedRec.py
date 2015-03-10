from RecommendationBase import User
from RecommendationBase import Movie
import RecommendationBase as base

def similarity_between_items(training_filename):
    matrix = base.matrix_from_filename(training_filename)
    user_ratings = base.ratings_by_user(matrix)
    movie_ratings = base.ratings_by_movie(user_ratings)

    movie_ids = movie_ratings.keys()
    distances = []
    for i in range(0, len(movie_ids)):
        movie_1_id = movie_ids[i]
        movie_1_raters = movie_ratings[movie_1_id]
        for j in range(i, len(movie_ids)):
            movie_2_id = movie_ids[j]
            movie_2_raters = movie_ratings[movie_2_id]



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tr', '--training', required=True, help='Filename for training set')
    parser.add_argument('-te', '--test', re)
    args = parser.parse_args()

if __name__ == '__main__':
    main()