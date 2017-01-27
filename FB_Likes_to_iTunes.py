#Facebook Likes to ITunes: 
#Return a file of links to iTunes (in table format) of the Facebook user's
#liked musicans, movies, books and actors

import unittest
import requests
import json

#Class of the user's liked music, movies, books, and tv shows
class User_Likes:
	def __init__(self, likes={}):
		self.user_name = ""
		self.musicians = []
		self.movies = []
		self.books = []
		self.tv = []
		if 'name' in likes:
			self.user_name = likes['name']
		if 'music' in likes:
			self.musicians = likes['music']['data']
		if 'movies' in likes:
			self.movies = likes['movies']['data']
		if 'books' in likes:
			self.books = likes['books']['data']
		if 'television' in likes:
			self.tv = likes['television']['data']

    #Sort each list by name
	def sort_likes(self):
		self.musicians = sorted(self.musicians, key = lambda k: k['name'])
		self.movies = sorted(self.movies, key = lambda k: k['name'])
		self.books = sorted(self.books, key = lambda k: k['name'])
		self.tv = sorted(self.tv, key = lambda k: k['name'])

	#Convert list of dictionaries to list of names/titles
	def names_only(self):
		temp = []
		for artist in self.musicians:
			temp.append(artist['name'])
		self.musicians = temp

		temp = []
		for movie in self.movies:
			temp.append(movie['name'])
		self.movies = temp

		temp = []
		for book in self.books:
			temp.append(book['name'])
		self.books = temp

		temp = []
		for show in self.tv:
			temp.append(show['name'])
		self.tv = temp

#Get access token and make facebook api request for the desired user's likes
def api_request(base, url_pars={}):
	r = requests.get(base, params=url_pars)
	d = json.loads(r.text)
	return d

#Create likes dictionary, parse by creating an instance of "User_Likes" class, then condense and sort using "names_only" sort method
def cache_or_live(option):

	if (option.lower() == "no"):
		#FB request info
		access_token = None
		if access_token is None:
 			access_token = raw_input("Copy and paste token from https://developers.facebook.com/tools/explorer. (*Note: Select 'user_likes' as the permission.)\n")
		url_params = {}
		url_params["access_token"] = access_token
		url_params["limit"] = 500
		url_params["fields"] = "name,music{name},movies{name},books{name},television{name}"
		base_url = "https://graph.facebook.com/me"

		likes_dict = api_request(base_url, url_params)

		outfile = open('fb_data.json', 'w')
		json.dump(likes_dict, outfile)
		outfile.close()
	
	else: #option = yes
		infile = open('fb_data.json', 'r')
		likes_dict = json.load(infile)
		infile.close()
		
	likes_info = User_Likes(likes_dict)
	likes_info.sort_likes()
	likes_info.names_only()

	return likes_info

def iTunes_links(fb_data, option):

	if(option.lower() == "no"):
		likes_links = {'music':[], 'movies':[], 'tv':[], 'books':[]}
		base_url = "https://itunes.apple.com/search"

		#Get artists links
		url_params = {}
		for artist in fb_data.musicians:
			url_params["term"] = artist
			url_params["media"] = 'music'
			url_params["limit"] = 500
			music_dict = api_request(base_url, url_params)

			#If a link exist in iTunes add it, if not return message
			try:
				likes_links['music'].append(music_dict['results'][0]['artistViewUrl'])
			except Exception:
				likes_links['music'].append("No link in iTunes Library")

		#Get movie links
		url_params = {}
		for movie in fb_data.movies:
			url_params["term"] = movie
			url_params["media"] = 'movie'
			url_params["limit"] = 500
			movie_dict = api_request(base_url, url_params)

			try:
				likes_links['movies'].append(movie_dict['results'][0]['collectionViewUrl'])
			except Exception:
				likes_links['movies'].append("No link in iTunes Library")

		#Get tv show links
		url_params = {}
		for show in fb_data.tv:
			url_params["term"] = show
			url_params["media"] = 'tvShow'
			url_params["limit"] = 500
			tv_dict = api_request(base_url, url_params)

			try:
				likes_links['tv'].append(tv_dict['results'][0]['collectionViewUrl'])
			except Exception:
				likes_links['tv'].append("Content not in iTunes Library")

		#Get book links
		url_params = {}
		for book in fb_data.books:
			url_params["term"] = book
			url_params["media"] = 'ebook'
			url_params["limit"] = 500
			book_dict = api_request(base_url, url_params)

			try:
				likes_links['books'].append(book_dict['results'][0]['trackViewUrl'])
			except Exception:
				likes_links['books'].append("Content not in iTunes Library")


		outfile = open('iTunes_data.json', 'w')
		json.dump(likes_links, outfile)
		outfile.close()
	else: #option == yes 
		infile = open('iTunes_data.json', 'r')
		likes_links = json.load(infile)
		infile.close()

	return likes_links

#Store data in .csv file in table format
def generate_output():
	source = raw_input("Do you want to used cached data? (Yes/No)\n")
	while (source.lower() != "no" and source.lower() != "yes"):
		source = raw_input("Invalid option entered. Do you want to used cached data? (Yes/No)\n")

	#Make get request to facebook api or get cache results
	try:
		fb_likes_data = cache_or_live(source)
	except Exception:
		print "No Cached Data Files Found. Use Live Data.\n"
		source = "no"
		fb_likes_data = cache_or_live(source)

	iTunes_links_data = iTunes_links(fb_likes_data, source)
	
	#For .csv output formatting***
	max_size = max(len(fb_likes_data.musicians), len(fb_likes_data.movies), len(fb_likes_data.tv), len(fb_likes_data.books))

	#Merge titles (fb_data_likes) with links(iTunes_links_data) into a dictionary
	merged_dict = {'music':[], 'movies':[], 'tv':[], 'books':[]}
	for i in range(max_size):
		try:
			merged_dict['music'].append(fb_likes_data.musicians[i] + ': ' + iTunes_links_data['music'][i])
		except Exception:
			merged_dict['music'].append("")
		try:
			merged_dict['movies'].append(fb_likes_data.movies[i] + ': ' + iTunes_links_data['movies'][i])
		except Exception:
			merged_dict['movies'].append("")
		try:
			merged_dict['tv'].append(fb_likes_data.tv[i] + ': ' + iTunes_links_data['tv'][i])
		except Exception:
			merged_dict['tv'].append("")
		try:
			merged_dict['books'].append(fb_likes_data.books[i] + ': ' + iTunes_links_data['books'][i])
		except Exception:
			merged_dict['books'].append("")

	#Generate .csv file
	outfile = open(fb_likes_data.user_name + '_likes.csv', 'w')
	outfile.write('"Links to Liked Music", "Links to Liked Movies", "Links to Liked TV Shows", "Links to Liked Books"\n')
	for item in range(max_size):
 		outfile.write('"{}", "{}", "{}, {}"\n'.format(merged_dict['music'][item], merged_dict['movies'][item], merged_dict['tv'][item], merged_dict['books'][item]))
	outfile.close()

	#For testing
	print "LINKS TO LIKED MEDIA GENERATED FOR: {}".format(fb_likes_data.user_name)
	return fb_likes_data


#Run Program and save returned instance for testing
test_inst = generate_output()


############################ TESTS #############################
User_Likes_1 = test_inst

class Tests_Cases(unittest.TestCase):
	def test_1(self):
		self.assertEqual(type(User_Likes_1), type(User_Likes()), "Testing that valid instance of User_Likes is generated.")

	def test_2(self):
		User_Likes_1.sort_likes # for test_3
		User_Likes_1.names_only
		self.assertEqual(type(User_Likes_1.musicians), type([]), "Testing names_only class method. Checking that test_1.musicians is now lists and not a dictionary.")

	def test_3(self):
		self.assertEqual(type(User_Likes_1.movies), type([]), "Testing names_only class method. Checking that test_1.movies is now lists and not a dictionary.")

	def test_4(self):
		self.assertEqual(type(User_Likes_1.tv), type([]), "Testing names_only class method. Checking that test_1.tv is now lists and not a dictionary.")

	def test_5(self):
		self.assertEqual(type(User_Likes_1.books), type([]), "Testing names_only class method. Checking that test_1.books is now lists and not a dictionary.")

	def test_6(self):
		User_Likes_2 = test_inst
		User_Likes_2.sort_likes
		User_Likes_2.names_only
		self.assertEqual(User_Likes_2.movies, User_Likes_1.movies, "Testing that sort_likes class methos returns sorted instances.")

unittest.main(verbosity=2)

































