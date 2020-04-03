from bs4 import BeautifulSoup
import requests

youtubeTestLink = 'https://www.youtube.com/playlist?list=PL67B0C9D86F829544'

res = requests.get(youtubeTestLink).text
soup = BeautifulSoup(res, features='lxml')

title = soup.select('div.pl-header-content h1.pl-header-title')
tags = soup.select('a.spf-link.yt-uix-sessionlink.yt-uix-tile-link.pl-video-title-link')

print(title[0].string.strip())

for tag in tags:
    print(tag.string.strip())
    #print(tag['href'][9:20])
