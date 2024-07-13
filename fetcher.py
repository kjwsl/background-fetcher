from pathlib import Path
import urllib.parse
import requests
import functools

from bs4 import BeautifulSoup

class WallpaperFlareImageFetcher:
    base_url = r"https://wallpaperflare.com/search?wallpaper="


    @functools.lru_cache(maxsize=5000)
    def download_image(self, url: str, query: str):
        response = requests.get(url)
        if response.status_code == 200:
            out_path = f"downloads/{query}"
            Path(out_path).mkdir(parents=True, exist_ok=True)
            with open(f"{out_path}/{url.split('/')[-1]}", "wb") as file:
                file.write(response.content)
        else:
            print(f"status code: {response.status_code}")



    def fetch_image_urls(self, query: str):
        url = self.base_url + urllib.parse.quote(query)
        ret = requests.get(url)
        soup = BeautifulSoup(ret.text, "html.parser")
        atags = soup.find_all("a", attrs={"itemprop": "url"})
        for atag in atags:
            ret = requests.get(f"{atag.get("href")}/download")
            soup = BeautifulSoup(ret.text,"html.parser")
            img = soup.find_all("img", attrs={"id":"show_img"})

            
            print(img[0].get("src"))

            self.download_image(img[0].get("src"), query)

