from multifetcher import WallpaperFlareImageFetcher

def main():

    query = input("Query: ")
    thread_cnt = input("Thread Number (default=10): ")
    if thread_cnt == "":
        thread_cnt = 10
    else:
        thread_cnt = int(thread_cnt)
    fetcher = WallpaperFlareImageFetcher(thread_cnt)
    fetcher.download_images(query)

if __name__ == "__main__":
    main()
