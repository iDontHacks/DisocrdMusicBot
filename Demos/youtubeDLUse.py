import youtube_dl
import json
import time
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

start = time.time()

ydl = youtube_dl.YoutubeDL({
    'ignoreerrors':True
    })
with ydl:
    result = ydl.extract_info(
        'https://www.youtube.com/playlist?list=PL08B5FA401C541429',
        download=False, # We just want to extract the info
    )
    
end = time.time()
duration = end - start
print('That operation took: ' + (time.strftime('%H:%M:%S', time.gmtime(duration))))

'''
if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries']
    for entry in video:
        entry['formats'] = []
    
else:
    # Just a video
    video = result


#print(json.dumps(video, sort_keys=False, indent=4))
'''
