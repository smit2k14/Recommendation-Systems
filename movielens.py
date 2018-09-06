import warnings
warnings.simplefilter('ignore', RuntimeWarning)
import pandas as pd
import tensorflow as tf
import numpy as np
import sklearn.metrics as sk

movie_tags = pd.read_csv('movies.csv')
	

class Movie:	
	unique_array = []	#This will count the number of genres in the given dataset

	def __init__(self):
		self.movie_id_tag = self.final_movie()
		self.len_genres = len(self.unique_array)
		self.genres_id = self.set_id_to_genres()

	def set_movies(self, movie_tag = movie_tags):   #This function is used to get the movies in ordered form ready to be parsed through
		movie_id_tag = {} # This contains the Name of the movies and it's genres
		count = 0
		for lines in movie_tags['genres']:
		    line = lines.split('|')
		    movie_id_tag[movie_tags['movieId'][count]] = line
		    count+=1
		    
		    for i in line:
		    	if i not in self.unique_array and i != '(no genres listed)':
		    		self.unique_array.append(i)
		return movie_id_tag
	
	def get_movie_tags(self):
		return self.movie_id_tag

	def get_length_genres(self):
		return self.len_genres

	def get_genres_id(self):
		return self.genres_id
	
	def set_id_to_genres(self):
		genres_id = {}
		count = 1
		for i in self.unique_array:
			genres_id[i] = count
			count+=1
		return genres_id

	def movie_genres_to_id(self):
		movie_id = self.set_movies()
		genres_id = self.set_id_to_genres()
		for movie in movie_id:
			count = 0
			for genres in movie_id[movie]:
				try:
					movie_id[movie][count] = genres_id[genres]
				except:
					movie_id[movie][count] = -1
					pass
				count+=1
		return movie_id

	def final_movie(self, movie_tag = movie_tags):
		movie_id = self.movie_genres_to_id()
		for movie in movie_id:
			contained_genres = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
			count = 0
			for genres in movie_id[movie]:
				if genres == -1:
					break
				else:
					contained_genres[genres-1] = 1
			movie_id[movie] = contained_genres
		return movie_id


users = pd.read_csv('ratings.csv')

class User:
	def __init__(self):
		self.user_ratings = self.set_user_matrix(num_movies = 164979)
	def set_user_matrix(self, num_movies, user = users):
		num_users = 671 
		user_ratings = np.zeros([num_users, num_movies])
		for i in range(num_users):
			idx = user.index[user['userId']==i+1].tolist()
			movie_id = user['movieId'].reindex(idx).tolist()
			movie_rating = user['rating'].reindex(idx).tolist()
			movie_id = list(map(lambda x: x-1, movie_id))
			user_ratings[i,movie_id] = movie_rating
			
		return user_ratings
	def similar_user(self, user, total_users):
		user = np.array(user).reshape(1, len(user))
		total_users = np.array(total_users)
		print(sk.pairwise.cosine_similarity(user, total_users))
				
user = User()
user_1 = user.user_ratings
user.similar_user(user_1[0], user_1)

