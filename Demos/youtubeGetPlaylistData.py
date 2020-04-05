from bs4 import BeautifulSoup
import requests

youtubeTestLink = 'https://www.youtube.com/playlist?list=PL08B5FA401C541429'

res = requests.get(youtubeTestLink).text
soup = BeautifulSoup(res, features='lxml')

title = soup.select('div.pl-header-content h1.pl-header-title')
tags = soup.select('a.spf-link.yt-uix-sessionlink.yt-uix-tile-link.pl-video-title-link')

print(title[0].string.strip() + '\n')

for tag in tags:
    print(tag)
    
