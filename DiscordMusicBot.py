import discord, os, sys, json, spotipy, webbrowser, io, urllib.parse, urllib.request, youtube_dl, asyncio, time, traceback, requests, random, re #regex
from bs4 import BeautifulSoup
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

FLAGS = {'offCommand':False, 'debug':True, 'calledNext': False, 'calledPrev':False, 'calledStop':False, 'goTo':[False,0], 'emergencyStop':False}

SONG_CHECK_GAP = 10

def logError(err):
        with open('errorLog.txt', 'a+') as file:
                file.write('Error logged at: ' + time.strftime("%H:%M:%S %d-%m-%Y", time.localtime()) + '\n')
                file.write('Error details as printed by python: \n' + str(err) + '\n')


def generateListImage(dataList):
        textWidth = len(max(dataList))
        height = len(dataList)
        lastButOne = len(dataList) - 1
        fontSize = 50

        # creating a image object
        image = Image.new('RGB', ((textWidth*fontSize)+10, (height*fontSize)+fontSize), color = (73, 109, 137))

        draw = ImageDraw.Draw(image)

        # specified font size
        font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', fontSize)

        text = ''

        for i in range(lastButOne):
                text += str(i) + ': ' + dataList[i] + '\n'

        text += str(lastButOne) + ': ' + dataList[lastButOne]

        # drawing text size
        draw.text((5, 5), text, font = font, align ="left")

        arr = io.BytesIO()
        image.save(arr, format='PNG')
        arr.seek(0)
        
        print('Done generateListImage')
        return arr


def getSpotifyPlaylist(urlOrUri):
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

                tracks.append(track['name'] + ' by ' + artist)
                #[Name of song and artist, duration of song]
                # duration of song is now legacy code
                              
        print('Done getSpotifyPlaylist')
        return playListName, tracks

def getSpotifySong(urlOrUri):
        testPlaylistLink = 'https://open.spotify.com/playlist/37i9dQZF1DX0s5kDXi1oC5?si=Kug95Nj8TKe9ZLXsu11ovg'
        testPlaylistURI = 'spotify:playlist:37i9dQZF1DX0s5kDXi1oC5'

        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) #create a spotify object

        trackObj = spotify.track(urlOrUri)
        artistURI = trackObj['artists'][0]['uri']
        artist = spotify.artist(artistURI)['name']

        track = [trackObj['name'] + ' by ' + artist, trackObj['duration_ms']]
        #[Name of song and artist, duration of song]
        # duration of song is now legacy code

        print('Done getSpotifySong')
        return track


def getYtLink(name):
        query_string = urllib.parse.urlencode({"search_query" : name}) #Convert uInput into url format
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string) #Go to website and return the html code for that site
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode()) #filter html code to links that have "watch?v={11 digit identifier}"

        if FLAGS['debug']:
                print('From getYtLink: ' + search_results[0])

        print('Done getYtLink')
        return ("http://www.youtube.com/watch?v=" + search_results[0]) #print the youtube video url followed by the first 11 digit identifer found by filter


def getYtPlaylist(url):
        res = requests.get(url).text
        soup = BeautifulSoup(res, features='lxml')
        tracks = []
        playlistName = ''
        youtubeVideoURL = "http://www.youtube.com/watch?v="

        playlistTitle =  soup.select('div.pl-header-content h1.pl-header-title')
        #h1 tag under the div tag
        tags = soup.select('a.spf-link.yt-uix-sessionlink.yt-uix-tile-link.pl-video-title-link')
        #pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link is what it looks like in the html tag

        if FLAGS['debug']:
                print('From getYtPlaylist (title): ')
                print(playlistTitle)
        
        for tag in tags:
                if FLAGS['debug']:
                        print('From getYtPlaylist: ' + tag.string.strip())
                        
                tracks.append(tag.string.strip())

        playlistName = playlistTitle[0].string.strip()
        
        return playlistName, tracks

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

@client.event
async def on_disconnect():
        print('Bot has Disconnected')
        await client.connect()
        print('Connect command passed')

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
async def next(ctx):
        FLAGS['calledNext'] = True
        print('Done next')

@client.command(pass_context=True)
async def prev(ctx):
        FLAGS['calledPrev'] = True
        print('Done prev')

@client.command(pass_context=True)
async def debug(ctx):
        if FLAGS['debug']:
                FLAGS['debug'] = False
        else:
                FLAGS['debug'] = True
        print('Done debug')

@client.command(pass_context=True)
async def goto(ctx, num):
        FLAGS['goTo'] = [True, int(num)]
        print('Done goto')

@client.command(pass_context=True)
async def play(ctx, url, ran=False):
        channel = ctx.channel
        i = 0
        skipCalled = False
        randCalled = []
        
        if 'youtube' in url:
                if 'playlist' in url:
                        playlistName, tracks = getYtPlaylist(url)
                        await channel.send('Now playing the playlist: ' + playlistName)

                        if not ran:
                                imageArr = generateListImage(tracks)
                                await channel.send(file = discord.File(imageArr, 'Playlist.png'))
                        else:
                                await channel.send('The playlist shall be played at random')

                        while (i <= len(tracks)) and (FLAGS['calledStop'] == False):
                                if ran and len(randCalled) <= len(tracks):
                                        if FLAGS['debug']:
                                                print('\nFrom play [random condition (randCalled before)]: ' + str(randCalled))
                                                print('From play [random condition (i before)]: ' + str(i))
                                        if randCalled == []:
                                                if FLAGS['debug']:
                                                        print('From play [random condition (first call)]')
                                                i = random.randrange(len(tracks))
                                                randCalled.append(i)
                                        else:
                                                i = random.randrange(len(tracks))
                                                if FLAGS['debug']:
                                                        print('From play [random condition (number genereated)]: ' + str(i))
                                                while (i in randCalled) and (len(randCalled) != len(tracks)):
                                                        i = random.randrange(len(tracks))
                                                        if FLAGS['debug']:
                                                                print('From play [random condition (number in list trying again)]: ' + str(i))

                                                randCalled.append(i)
                                                
                                        if FLAGS['debug']:
                                                print('From play [random condition (randCalled after)]: ' + str(randCalled))
                                                print('From play [random condition (i after)]' + str(i))
                                                
                                if FLAGS['debug']:
                                        print('\nFrom play [before code]: ' + str(i))

                                if FLAGS['goTo'][0]:
                                        if FLAGS['debug']:
                                                print('From play [goTo flag triggered (i before)]: ' + str(i))

                                        i = FLAGS['goTo'][1]
                                        FLAGS['goTo'][0] = False
                                        FLAGS['goTo'][1] = 0
                                        gotoCalled = True
                                        
                                        if FLAGS['debug']:
                                                print('From play [goTo flag triggered (i after)]: ' + str(i))
                                
                                try:
                                        guild = ctx.message.guild
                                        voice_client = guild.voice_client

                                        if not voice_client.is_playing():
                                                if FLAGS['debug']:
                                                        print('\nFrom Play [index]: ' + str(i))
                                                        print('From play [name]: ' + tracks[i])
                                                        
                                                ytUrl = getYtLink(tracks[i])
                                                check = downloadAudio(ytUrl)
                                                if check:
                                                        voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
                                                        await channel.send('Now playing: ' + tracks[i])

                                                        while voice_client.is_playing() or voice_client.is_paused():
                                                                if FLAGS['calledNext']:
                                                                        i += 1
                                                                        FLAGS['calledNext'] = False
                                                                        skipCalled = True
                                                                        voice_client.stop()
                                                                        break
                                                                elif FLAGS['calledPrev']:
                                                                        i -= 1
                                                                        FLAGS['calledPrev'] = False
                                                                        skipCalled = True
                                                                        voice_client.stop()
                                                                        break
                                                                elif FLAGS['goTo'][0]:
                                                                        i = FLAGS['goTo'][1]
                                                                        FLAGS['goTo'][0] = False
                                                                        FLAGS['goTo'][1] = 0
                                                                        skipCalled = True
                                                                        voice_client.stop()
                                                                        break
                                                                else:
                                                                        await asyncio.sleep(SONG_CHECK_GAP)
                                except Exception:
                                        logError(traceback.format_exc())
                                finally:
                                        if not FLAGS['offCommand']:
                                                if not skipCalled:
                                                        i += 1
                                                skipCalled = False
                                        else:
                                                break
                else:
                        check = downloadAudio(url)
                        if check:
                                guild = ctx.message.guild
                                voice_client = guild.voice_client
                                voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
        elif 'spotify' in url:
                if 'playlist' in url:
                        playlistName, tracks = getSpotifyPlaylist(url)
                        await channel.send('Now playing the playlist: ' + playlistName)

                        if not ran:
                                imageArr = generateListImage(tracks)
                                await channel.send(file = discord.File(imageArr, 'Playlist.png'))
                        else:
                                await channel.send('The playlist shall be played at random')

                        while (i <= len(tracks)) and (FLAGS['calledStop'] == False):
                                if ran and len(randCalled) <= len(tracks):
                                        if randcalled == []:                                                
                                                i = random.randrange(len(tracks))
                                                randCalled.append(i)
                                        else:
                                                i = random.randrange(len(tracks))
                                                while (i in randCalled) and (len(randCalled) != len(tracks)):
                                                        i = random.randrange(len(tracks))
                                                randCalled.append(i)
                                                
                                if FLAGS['goTo'][0]:
                                        i = FLAGS['goTo'][1]
                                        FLAGS['goTo'][0] = False
                                        FLAGS['goTo'][1] = 0
                                        gotoCalled = True
                                        
                                try:
                                        guild = ctx.message.guild
                                        voice_client = guild.voice_client

                                        if not voice_client.is_playing():
                                                ytUrl = getYtLink(tracks[i])
                                                check = downloadAudio(ytUrl)
                                                if check:
                                                        voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
                                                        await channel.send('Now playing: ' + tracks[i])
                                        else:
                                                while voice_client.is_playing() or voice_client.is_paused():
                                                        if FLAGS['calledNext']:
                                                                i += 1
                                                                FLAGS['calledNext'] = False
                                                                skipCalled = True
                                                                voice_client.stop()
                                                                break
                                                        elif FLAGS['calledPrev']:
                                                                i -= 1
                                                                FLAGS['calledPrev'] = False
                                                                skipCalled = True
                                                                voice_client.stop()
                                                                break
                                                        elif gotoCalled:
                                                                i = FLAGS['goTo'][1]
                                                                FLAGS['goTo'][0] = False
                                                                FLAGS['goTo'][1] = 0
                                                                skipCalled = True
                                                                voice_client.stop()
                                                                break
                                                        else:
                                                                await asyncio.sleep(SONG_CHECK_GAP)  
                                except Exception:
                                        logError(traceback.format_exc())
                                finally:
                                        if not FLAGS['offCommand']:
                                                if not skipCalled:
                                                        i += 1
                                                skipCalled = False
                                        else:
                                                break
                elif 'track' in url:
                        track = getSpotifySong(url)
                        try:
                                guild = ctx.message.guild
                                voice_client = guild.voice_client

                                if not voice_client.is_playing():
                                        ytUrl = getYtLink(track[0])
                                        check = downloadAudio(ytUrl)
                                        if check:
                                                voice_client.play(discord.FFmpegPCMAudio("song.mp3"))
                                                await channel.send('Now playing: ' + track[0])
                                else:
                                        await asyncio.sleep(SONG_CHECK_GAP)
                        except Exception:
                                logError(traceback.format_exc())
                                await channel.send('The system has encountered an unexpected error, please try again later')
                else:
                        await channel.send('The system for that is not set up yet')

        else:
            await channel.send('The system only set up for youtube and spotify')

        i = 0
        FLAGS['calledStop'] = False

        if FLAGS['emergencyStop']:
                await channel.send('The Bot has encountered an unexpected error, please try again after fixing')
        
        FLAGS['emergencyStop'] = False
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
        FLAGS['calledStop'] = True
        print('Done stop')

@client.command(pass_context=True)
async def off(ctx):
        FLAGS['offCommand']=True
        print('Off command passed')
        await client.logout()

client.run(TOKEN)
