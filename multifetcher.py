from pathlib import Path
import urllib.parse
import requests
import functools
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

class WallpaperFlareImageFetcher:
    base_url = r"https://wallpaperflare.com/"
    query_url = r"https://wallpaperflare.com/search?wallpaper="

    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    @functools.lru_cache(maxsize=5000)
    def download_image(self, url: str, query: str):
        filename = url.split("/")[-1]

        print(f"Downloading from {filename}")
        response = requests.get(url)
        if response.status_code == 200:
            out_path = f"downloads/{query}"
            Path(out_path).mkdir(parents=True, exist_ok=True)
            with open(f"{out_path}/{filename}", "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download {url} - status code: {response.status_code}")

    def fetch_image_urls(self, query: str):
        print("Fetching images...")
        url = self.query_url + urllib.parse.quote(query)
        ret = requests.get(url)
        if ret.url == self.base_url:
            print("No Image Found")
            return
        
        soup = BeautifulSoup(ret.text, "html.parser")
        atags = soup.find_all("a", attrs={"itemprop": "url"})
        image_urls = []
        
        for atag in atags:
            detail_url = f"{atag.get('href')}/download"
            ret = requests.get(detail_url)
            soup = BeautifulSoup(ret.text, "html.parser")
            img = soup.find_all("img", attrs={"id": "show_img"})
            if len(img):
                image_urls.append(img[0].get("src"))

        return image_urls

    def download_images(self, query: str):
        image_urls = self.fetch_image_urls(query)
        futures = [self.executor.submit(self.download_image, url, query) for url in image_urls]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error downloading image: {e}")

    def __del__(self):
        self.executor.shutdown(wait=True)
