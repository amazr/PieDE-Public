from __future__ import unicode_literals
import youtube_dl
import requests
import json
import os

import googleapiclient.discovery

def main(searchKeyword):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "Developer key here"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=searchKeyword,
        type="id"
    )
    response = request.execute()

    print(response)

#creates a temp mp3 file from a youtube video. Stores it in temp-audio.mp3
def createAudio(url):
    try:
        os.remove("temp-audio.mp3")
    except OSError:
        pass
    options = {
        'format': 'bestaudio/best',
        'extractaudio' : True,  # only keep the audio
        'audioquality' : 0,
        'audioformat' : "mp3",  # convert to mp3 
        'outtmpl': 'temp-audio.mp3',    # name the file the ID of the video
        'noplaylist' : True,    # only download single song, not playlist
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    main("use this gospel")