import discord, os, sys, json, spotipy, webbrowser, io, urllib.parse, urllib.request, youtube_dl, asyncio, time, traceback, re #regex
from discord.ext import commands
from json.decoder import JSONDecoder
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image, ImageFont, ImageDraw

#Discord related info
TOKEN = 'NTM3MzczMTU5ODc2MTk4NDAw.XnfPcQ.quxF8FZ3E7tgWUNrFzJb1Iy_jJQ'
client = commands.Bot(command_prefix = '.')
BOT_NAME = 'Music Player'

#Spotify related info
CLIENT_ID = '5bdb9ae41cfb465391bb6184996f97ae'
CLIENT_SECRET = '9ca3934ab64549e9b24859362dda92e9'

FLAGS = {'offCommand':False}

def logError(err):
        with open('errorLog.txt', 'a+') as file:
                file.write('Error logged at: ' + time.strftime("%H:%M:%S %d-%m-%Y", time.localtime()) + '\n')
                file.write('Error details as printed by python: \n' + str(err) + '\n')


def generateListImage(dataList):
        textWidth = len(max(dataList))
        height = len(dataList)
        fontSize = 50

        # creating a image object  
        image = Image.new('RGB', ((textWidth*fontSize)+10, (height*fontSize)+fontSize), color = (73, 109, 137))

        draw = ImageDraw.Draw(image)  

        # specified font size 
        font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', fontSize)  

        text = ''

        for i in range(len(dataList) - 1):
                text += dataList[i] + '\n'

        text += dataList[len(dataList) - 1]

        # drawing text size 
        draw.text((5, 5), text, font = font, align ="left")  

        print('Done generateListImage')
        return image
        

def getPlaylist(urlOrUri):
        testPlaylistLink = 'https://open.spotify.com/playlist/37i9dQZF1DX0s5kDXi1oC5?si=Kug95Nj8TKe9ZLXsu11ovg'
        testPlaylistURI = 'spotify:playlist:37i9dQZF1DX0s5kDXi1oC5'
        
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) #create a spotify object

        playlistJSON = spotify.playlist(urlOrUri)
        playListName = playlistJSON['name']
        trackURIs = []
        tracks = []

        for i in range(len(playlistJSON['tracks']['items'])):
                trackURIs.append(playlistJSON['tracks']['items'][i]['track']['uri'])

        for i in range(len(trackURIs)):
                track = spotify.track(trackURIs[i])
                artistURI = track['artists'][0]['uri']
                artist = spotify.artist(artistURI)['name']
                
                tracks.append([track['name'] + ' by ' + artist, track['duration_ms'], track['name']])

        print('Done getPlaylist')
        return playListName, tracks


def getYtLink(name):
        query_string = urllib.parse.urlencode({"search_query" : name}) #Convert uInput into url format
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) #Go to website and return the html code for that site
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) #filter html code to links that have "watch?v={11 digit identifier}"
        print('Done getYtLink')
        return ("http://www.youtube.com/watch?v=" + search_results[0]) #print the youtube video url followed by the first 11 digit identifer found by filter


def downloadAudio(url):
        ydl_opts = {
                'ignoreerrors':True,
                'format': 'bestaudio/best',
                'outtmpl': u'song.%(ext)s',
                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        print('Done downloadAudio')
        return True

        
@client.event
async def on_ready():
        os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
        os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
        print('Bot Online')
	
@client.command(pass_context=True)
async def join(ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        print('Done join')

@client.command(pass_context=True)
async def leave(ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()
        print('Done leave')

@client.command(pass_context=True)
async def play(ctx, url):
        channel = ctx.channel
        if 'youtube' in url:
                if 'playlist' in url:
                        await channel.send('The system for that is not set up yet')
                else:
                        check = downloadAudio(url)
                        if check:
                                guild = ctx.message.guild
                                voice_client = guild.voice_client
                                voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
        elif 'spotify' in url:
                if 'playlist' in url:
                        playlistName, tracks = getPlaylist(url)
                        await channel.send('Now playing the playlist: ' + playlistName)
                        
                        for track in tracks:
                                try:
                                        ytUrl = getYtLink(track[0])
                                        check = downloadAudio(ytUrl)
                                        if check:
                                                guild = ctx.message.guild
                                                voice_client = guild.voice_client
                                                voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
                                                await channel.send('Now playing: ' + track[2])
                                                await asyncio.sleep( (track[1] / 1000) + 2 )
                                except Exception:
                                        logError(traceback.format_exc())
                                finally:
                                        if not FLAGS['offCommand']:
                                                pass
                                        else:
                                                break
                else:
                        await channel.send('The system for that is not set up yet')

        else:
            await channel.send('The system only set up for youtube and spotify')

        print('Done play')

@client.command(pass_context=True)
async def pause(ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        voice_client.pause()
        print('Done pause')
        
@client.command(pass_context=True)
async def resume(ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        voice_client.resume()
        print('Done resume')
        
@client.command(pass_context=True)
async def stop(ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        voice_client.stop()
        print('Done stop')

@client.command(pass_context=True)
async def getTracks(ctx):
        channel = ctx.channel
        plName, tracks = getPlaylist()       

        listImage = generateListImage(tracks)

        arr = io.BytesIO()
        listImage.save(arr, format='PNG')
        arr.seek(0)

        await channel.send(file = discord.File(arr, 'Playlist.png'))
        print('Done getTracks')
        
@client.command(pass_context=True)
async def off(ctx):
        FLAGS['offCommand']=True
        print('Off command passed')
        await client.logout()
	
client.run(TOKEN)
