Facebook Likes to iTunes:

-Overview

My project collects a Facebook user’s liked media content (music, movies, tv shows, and books) and generates links to that content (if applicable) in the Apple iTunes store. These links are then returned to the user in a csv file in table format. The name of csv file will be (Facebook Username)_likes.csv. This allows a user to easily find they type of media that they’re interested in purchasing.  


-Directions:

First run FB_Likes_to_iTunes.py in python and follow the directions on the prompt.
The first prompt will ask if you want to use cached or live data by entering “yes” or “no” (if invalid input is given a help message will appear).
If you enter “no” (use live data) another prompt will appear with directions for getting a Facebook api access token.
After you get the access token copy and paste it into the terminal and press enter to finish running the program.
After the program finishes running, a new file of iTunes media links called “(Facebook Username)_likes.csv” will be generated along with new cached data files (fb_data.json and iTunes_data.json) with information from this iteration of the program for future use.
If “yes” is selected (use cached data) the program will use cached data files from a previous iteration of the program in order to generate the csv file of iTunes media links.


-Files:

FB_Likes_to_iTunes.py: Python executable file to run the program.
fb_data.json: Cached Facebook user likes information (users name and liked music, movies, tv shows, and books).
iTunes_data.json: Cached iTunes Search links based on user likes in fb_data.json.
README.txt: Text file describing details of the program.


-Required Packages/Modules:

Packages: unittest, requests, json

-Data Sources:

Facebook Graph API Explorer: https://developers.facebook.com/tools-and-support/
iTunes Search API: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/


-Summary:

I decided to do this project because I found it extremely tedious searching iTunes for music, movies, tv shows and books that I like. I figured since the information about the specific types of media that I like were already on my Facebook page, I’d just write a program that automatically searches for me saving a lot of time.