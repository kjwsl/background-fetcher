from multifetcher import WallpaperFlareImageFetcher

def main():
    fetcher = WallpaperFlareImageFetcher()

    query = input("Query: ")
    fetcher.download_images(query)

if __name__ == "__main__":
    main()
