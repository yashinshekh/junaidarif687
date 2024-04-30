# yt-dlp https://www.pornhub.com/view_video.php?viewkey=655242c3d841d

import yt_dlp
import os
import glob
import scrapy
import requests
import concurrent.futures
import csv

def download_video(video_url):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{os.getcwd()}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])


    try:
        os.system("sudo rm -r *.mp4*")
    except:
        pass





if __name__ == "__main__":

    while True:

        with open('link.csv','r') as r:
            reader = csv.reader(r)

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as f:
                a = {
                    f.submit(download_video,line[0])
                    for line in reader
                }


