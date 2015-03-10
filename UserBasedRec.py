from RecommendationBase import User
import RecommendationBase as base
import argparse
import math
import operator

"""
UserBasedRec.py by Brian Charous and Yawen Chen
An implementation of recommendation system with movie data, using item based approach

We have three files related to this project:
    RecommendationBase.py
    ItemBasedRec.py
    UserBasedRec.py

To compile: python UserBasedRec -tr (training_filename) -te (test_filename) -k (optional, k_nearest neighbors) -n(optional, min number of movies user share)
e.g: python UserBasedRec.py -tr ua.base -te ua.test -k 10 
"""
def predict_ratings_user(training_file_name, test_file_name, k=10, n=10):
	data = base.matrix_from_filename(training_file_name)
	users = base.ratings_by_user(data) # a dictionary of user objects with their ratings for each movie
    	data_test = base.matrix_from_filename(test_file_name)
    	recs_made = 0
    	predict_users_dict ={}
    	prediction_list = []
    	error_by_user={}
    	occurrences_of_user = {}
    	for row in data_test:
    		i = 0
    		count = 0
    		prediction = 0
    		uid = row[0]
    		mid = row[1]
    		real_rating = row[2]
    		if uid not in predict_users_dict:
			sorted_distance = compute_distance(uid, users)
			predict_users_dict[uid] = sorted_distance
		while count < k:
			if i== len(predict_users_dict[uid]):
				break
			cur_user = predict_users_dict[uid][i][1]
			if cur_user.has_rated_movie(mid):
				prediction += cur_user.ratings[mid]
				count += 1
				i+= 1
			else: 
				i+=1
		prediction = prediction/float(count)+ users[uid].mean	
		prediction_list.append((row, prediction))
		# total error
		error += (real_rating - prediction) **2
		recs_made += 1

		# keep track of error by user
		if uid not in error_by_user:
                    		error_by_user[uid] = 0
                    	error_by_user[uid] += (real_rating - prediction)**2

                	 # keep track of # of times we've seen each user
                	if uid not in occurrences_of_user:
                    		occurrences_of_user[uid] = 0
                		occurrences_of_user[uid] += 1
		print "The predicted rating for user {0} on movie {1} is {2}, and the actual rating is{3}: \n".format(row[0], row[1], prediction, row[2])

	# calculate error for each user
    	for user in error_by_user:
        		occurrences = occurrences_of_user[user]
        		error_by_user[user] = math.sqrt(error_by_user[user]/occurrences)

	sorted_by_error = sorted(error_by_user.items(), key=operator.itemgetter(1))
	print "Best predicted user:"
	for best in sorted_by_error[:10]:
	    print best[0]
	print
	print "Worst predicted user:"
	for worst in sorted_by_error[-10:]:
	    print worst[0]
	print

    	rmse = math.sqrt(error/recs_made)
    	print "Total RMSE: {0}".format(rmse)
	#for j in range(len(prediction_list)):
    		#print "The predicted rating for user {0} on movie {1} is {2}, and the actual rating is{3}: /n".format(prediction_list[j][0][0], prediction_list[j][0][1], prediction_list[j][1], prediction_list[j][0][2])
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
	#print sorted_distance [1]
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