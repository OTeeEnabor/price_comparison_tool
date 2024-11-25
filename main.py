import time
from web_scrape.store_scrape import StoreScraper

if __name__ == "__main__":
    start = time.perf_counter()

    # initialize a StoreScraper object
    store_scraper = StoreScraper()
    # get product urls
    store_scraper.get_product_urls()

    # # get product data
    # store_scraper.get_product_data()

    # # process the raw data
    # store_scraper.process_product_data()

    # # upload the processed data
    # store_scraper.upload_products() 

    # # get finish time
    # finish = time.perf_counter()
    
    # # print duration of script
    # print(f"finished in {round(finish-start,2)} seconds (s)")
