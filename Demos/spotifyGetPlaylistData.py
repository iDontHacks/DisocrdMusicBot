import os, sys, json, spotipy, webbrowser
from json.decoder import JSONDecoder
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image, ImageFont, ImageDraw  

def generateListImage(dataList):
    textWidth = len(max(dataList))
    height = len(dataList)
    
    # creating a image object  
    image = Image.new('RGB', ((textWidth*20)+10, (height*20)+20), color = (73, 109, 137))
      
    draw = ImageDraw.Draw(image)  
      
    # specified font size 
    font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 20)  
      
    text = ''

    for i in range(len(dataList) - 1):
        text += dataList[i] + '\n'

    text += dataList[len(dataList) - 1]
      
    # drawing text size 
    draw.text((5, 5), text, font = font, align ="left")  
      
    image.show()  


CLIENT_ID = '5bdb9ae41cfb465391bb6184996f97ae'
CLIENT_SECRET = '9ca3934ab64549e9b24859362dda92e9'

os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET

testPlaylistLink = 'https://open.spotify.com/playlist/37i9dQZF1DX0s5kDXi1oC5?si=Kug95Nj8TKe9ZLXsu11ovg'

testPlaylistURI = 'spotify:playlist:37i9dQZF1DX0s5kDXi1oC5'

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) #create a spotify object

testPlaylist = spotify.playlist(testPlaylistLink)
trackURIs = []
tracks = []

for i in range(len(testPlaylist['tracks']['items'])):
    trackURIs.append(testPlaylist['tracks']['items'][i]['track']['uri'])

for i in range(len(trackURIs)):
    track = spotify.track(trackURIs[i])
    artistURI = track['artists'][0]['uri']
    artist = spotify.artist(artistURI)['name']
    
    tracks.append(str(i) + ': ' + track['name'] + ' by ' + artist)

print(spotify.track(trackURIs[0])['name'])
