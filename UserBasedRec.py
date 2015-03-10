from RecommendationBase import User
import RecommendationBase as base
import argparse

def predict_ratings_user(training_file_name, test_file_name, k=10, n=10):
	data = base.matrix_from_filename(training_file_name)
	users = base.ratings_by_user(data) # a dictionary of user objects with their ratings for each movie
    	data_test = base.matrix_from_filename(test_file_name)
    	predict_users_dict ={}
    	prediction_list = []
    	for row in data_test:
    		i = 0
    		count = 0
    		prediction = 0
    		uid = row[0]
    		mid = row[1]
    		#real_rating = row[2]
    		if uid not in predict_users_dict:
			sorted_distance = compute_distance(uid, users)
			predict_users_dict[uid] = sorted_distance
		while count < k:
			cur_user = predict_users_dict[uid][i][1]
			if cur_user.has_rated_movie(mid):
				prediction += cur_user.ratings[mid]
				count += 1
				i+= 1
			else: 
				i+=1
		prediction = prediction/k		
		prediction_list.append(tuple(row, prediction))
		print "The predicted rating for user {0} on movie {1} is, and the actual rating is{2: ".format(row[0], row[1], prediction, row[3])
    	return prediction_list

def compute_distance(uid, users):
	distance = []
	for userid, user_object in users.iteritems():
		#print "useird is:{0}".format(userid)
		#print users[uid]
    		if userid != uid:
    			cur_user_object = user_object 
    			dist = base.cosine_distance(users[uid], user_object)
    			dist_user = (dist, cur_user_object)
    			distance.append(dist_user)
	sorted_distance = sorted(distance, key = getKey)
	print sorted_distance [1]
	return sorted_distance	

def getKey(item):
    return item[0]


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-tr', '--training', required=True, help='Filename for training set')
	parser.add_argument('-te', '--test', required = True, help= 'Filename for testing set')
	parser.add_argument('-k', '--k_nearest', required = False, help = ' define the number nearest neighbors')
	parser.add_argument('-n', '--n', required = False, help ='the number of movies users share in common for them to be considered the near')
	args = parser.parse_args()

	predict_ratings_user(args.training, args.test, args.k_nearest)
    #print users[109].ratings
    
if __name__ == '__main__':
    main()