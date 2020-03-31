import urllib.request
import urllib.parse
import re #regex

youtubeSearchURL = "http://www.youtube.com/results?"
#This is the begining of the url that comes up when you search something on youtube

youtubeVideoURL = "http://www.youtube.com/watch?v="
#This is the begining of the url that comes up when you watch a video on youtube

uInput = input()
query_string = urllib.parse.urlencode({"search_query" : uInput}) #Convert uInput into url format
html_content = urllib.request.urlopen(youtubeSearchURL + query_string) #Go to website and return the html code for that site
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) #filter html code to links that have "watch?v={11 digit identifier}"
print(youtubeVideoURL + search_results[0]) #print the youtube video url followed by the first 11 digit identifer found by filter
