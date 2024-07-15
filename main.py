import os
from datetime import date
import concurrent.futures
import time
import numpy as np
import pandas as pd
import pprint
from pathlib import Path

import web_scrape
from web_scrape import helpers
from web_scrape import selenium_scrape
from web_scrape.store_scrape import StoreScraper
from web_scrape.selenium_scrape import (
    get_woolies_product_data,
    get_checkers_product_data,
)



if __name__ == "__main__":
    start = time.perf_counter()

    # initialize a StoreScraper object
    store_scraper = StoreScraper(date_stamp="20240712")
  
    # get product urls
    # store_scraper.get_product_urls()

    # get product data
    store_scraper.get_product_data()

    # process the raw data
    # store_scraper.process_[plproduct_data()

    # upload the processed data
    # store_scraper.upload_products()

# # get product csv dict
# product_url_dict = store_scraper.get_product_csv_dict("2024626")

# for store, csv_list in product_url_dict.items():
#     if __name__ == "__main__":
#         if store == "Woolworths":
#             with concurrent.futures.ProcessPoolExecutor() as executor:
#                 results = executor.map(get_woolies_product_data, csv_list)
#                 output_list = []
#                 for result in results:
#                     list_result = list(result)
#                     print(list_result)
#                     output_list.append(list_result)
#         if store == "Checkers":
#             with concurrent.futures.ProcessPoolExecutor() as executor:
#                 results = executor.map(get_checkers_product_data, csv_list)
#                 output_list = []
#                 for result in results:
#                     list_result = list(result)
#                     print(list_result)
#                     output_list.append(list_result)
#         results = list(np.concatenate(output_list).flat)
#         # create output csv
#         product_data_df = pd.DataFrame(results)
#         print(product_data_df.head())
#         # save to csv
#         product_data_df.to_csv(
#             store_scraper.storage_path
#             + f"{store}\\{store_scraper.date_stamp}\\{store}_product_data\\products_data_{store_scraper.date_stamp}.csv",
#             index=False,
#         )

    finish = time.perf_counter()

    print(f"finished in {round(finish-start,2)} seconds (s)")
# # get the current date
# current_date = date.today()

# # define date stamp
# date_stamp = f"{current_date.year}{current_date.month}{current_date.day}"

# # get the product category information
# store_information_dict = helpers.get_store_url_dict(r"Store_Category_Sheet.xlsx")

# # create the storage path
# storage_path = os.getcwd() +f"\\data\\stores\\"

# for store, category_dict in store_information_dict.items():
#     # create directory
#     helpers.create_directory(storage_path+f"{store}\\{date_stamp}")
#     for category, category_url in category_dict.items():
#         # create directory to store product urls
#         product_url_path = storage_path+f"{store}\\{date_stamp}\\{store}_product_urls"
#         helpers.create_directory(product_url_path)
#         # get the scrape product urls
#         category_product_links = selenium_scrape.url_scraper(category_url=category_url)
#         # write to csv
#         helpers.create_product_urls_csv(product_urls_list=category_product_links, product_category=helpers.sanitize_category(category),current_date=current_date, store_path=product_url_path)

# pprint.pprint(store_information_dict)


# print(helpers.sanitize_category("Dairy, Eggs & Milk.csv"))


# # get current working path s

# cwd = os.getcwd()
# # create directory
# # test_path = "\\data\\stores\\random"
# # create_directory(cwd+test_path)
# # print(cwd)

# spreadsheet_name = "Store_Category_Sheet.xlsx"

# spreadsheet_path = cwd+ "\\data\\" + spreadsheet_name

# # save store information dictionary containing store and category url information
# store_information_dict = get_store_url_dict(spreadsheet_path)

# for store, category_dict in store_information_dict.items():
#     for category, category_url in category_dict.items():
#         # collect product urls
#         category_product_links = selenium_scrape.url_scraper(category_url=category_url)
