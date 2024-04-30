import scrapy
import wget
import os
import glob
import yt_dlp
import csv

class PornhubSpider(scrapy.Spider):
    name = "pornhub"
    start_urls = ["https://pornhub.com"]

    custom_settings = {
        "CONCURRENT_REQUESTS":1
    }


    def start_requests(self):
        for i in range(1,343):
            # print("Hello")
            yield scrapy.Request(f'https://www.pornhub.com/video?page={i}',callback=self.parse)
            # break

    def parse(self, response,*args):
        links = response.xpath('.//*[@class="title"]/a/@href').extract()

        for link in links:
            with open("link.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow(['https://www.pornhub.com'+link])
                print(['https://www.pornhub.com'+link])

    #     print(links)
    #
    #     for link in links:
    #
    #         options = {
    #             'format': 'bestvideo+bestaudio/best',
    #             'outtmpl': f'{os.getcwd()}/%(title)s.%(ext)s',
    #         }
    #
    #         with yt_dlp.YoutubeDL(options) as ydl:
    #             # ydl.download(['https://www.pornhub.com'+link])
    #
    #             info_dict = ydl.extract_info('https://www.pornhub.com'+link, download=True)
    #             file_name = ydl.prepare_filename(info_dict)
    #
    #             print(file_name)
    #             os.remove(file_name)
    #
    #         try:
    #             os.system("sudo rm -r *.mp4*")
    #         except:
    #             pass
    #
    # def close(spider, reason):
    #
    #     directory = os.getcwd()
    #     try:
    #         # Use glob to find all .mp4 files in the specified directory
    #         mp4_files = glob.glob(os.path.join(directory, "*.mp4*"))
    #         parts = glob.glob(os.path.join(directory, "*.part*"))
    #         ytdls = glob.glob(os.path.join(directory, "*.ytdl*"))
    #
    #         try:
    #             for part in parts:
    #                 os.remove(part)
    #         except:
    #             pass
    #
    #         try:
    #             for yt in ytdls:
    #                 os.remove(yt)
    #         except:
    #             pass
    #
    #         if not mp4_files:
    #             print(f"No .mp4 files found in {directory}.")
    #             return
    #
    #         # Iterate through the list of .mp4 files and delete each one
    #         for mp4_file in mp4_files:
    #             os.remove(mp4_file)
    #             print(f"File {mp4_file} deleted successfully.")
    #
    #     except Exception as e:
    #         print(f"An error occurred: {str(e)}")
    #
    #
    #     print("@@@@@@@@")
    #     os.system("scrapy runspider pornhub.py")