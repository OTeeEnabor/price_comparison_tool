from datetime import date
import concurrent.futures
import itertools
import sys
import logging
import os
import numpy as np
import pandas as pd
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from . import helpers, selenium_scrape

# append project directory

PROJECT_PATH = Path.cwd()

sys.path.append(str(PROJECT_PATH))

from utils import database


class StoreScraper:
    """
     The StoreScraper object is used to scrape product information from store website.

    :param date_stamp (str): date to assign product information

    Attributes:
    : current_date (str): today's date
    : store_information_dict (dict): dictionary containing store information to scrape
    : storage_path (str): path to store data

    """

    def __init__(self, date_stamp=None):
        # initialize current date
        self.current_date = date.today()
        self.current_date_month = "{:02d}".format(self.current_date.month)
        # initialize date stamp
        if date_stamp == None:
            self.date_stamp = f"{self.current_date.year}{self.current_date_month}{self.current_date.day}"
        else:
            self.date_stamp = date_stamp
        # initialize store information dictionary
        self.store_information_dict = helpers.get_store_url_dict(
            r"Store_Category_Sheet.xlsx"
        )
        # initialize storage path
        self.storage_path = Path.cwd() / "data" / "stores"
        # log when Store Scraper is created
        # create StoreScraper Logger
        self.store_scraper_logger = logging.getLogger(__name__)
        # set logger level to information
        self.store_scraper_logger.setLevel(logging.INFO)

        # log_file_location
        log_file_location = (
            Path.cwd()
            / "logs"
            / "store_scraper"
            / f"store_scraper_obj_{self.date_stamp}.log"
        )
        # define configuration for logger
        log_config = {
            "FORMATTER_FORMAT": "%(levelname)s - %(asctime)s - %(name)s: -%(message)s",
            "LOG_FILE": log_file_location,
        }

        formatter = logging.Formatter(log_config["FORMATTER_FORMAT"])
        file_handler = logging.FileHandler(log_config["LOG_FILE"])
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.store_scraper_logger.addHandler(file_handler)

        self.store_scraper_logger.info("StoreScraper object created!")

    def get_product_urls(self):
        """
        Creates a csv for each product category for each store in the information sheet.

        """
        # define date stamp
        date_stamp = self.date_stamp

        # get the store category information
        store_information_dict = self.store_information_dict

        # get the storage path
        storage_path = self.storage_path

        # iterate through the store information dictionary
        for store, category_dict in store_information_dict.items():
            # create the directory for current date
            current_date_directory = storage_path / f"{store}" / f"{date_stamp}"
            helpers.create_directory(current_date_directory)
            # create directory to store product urls
            product_url_path = (
                storage_path / f"{store}" / f"{date_stamp}" / f"{store}_product_urls"
            )
            helpers.create_directory(product_url_path)
            # create directory to store product url data
            product_data_path = (
                storage_path / f"{store}" / f"{date_stamp}" / f"{store}_product_data"
            )
            helpers.create_directory(product_data_path)
            # create raw and processed data
            helpers.create_directory(product_data_path / "raw")
            helpers.create_directory(product_data_path / "processed")
            # access the information on the sheet
            for category, category_url in category_dict.items():
                # get product urls from internet - scraping starts now
                category_product_links = selenium_scrape.url_scraper(
                    category_url=category_url, store=store
                )
                # sanitize category string to remove unwanted characters and whitespaces
                sanitized_category = helpers.sanitize_category(category)
                # write product urls to csv
                helpers.create_product_urls_csv(
                    category_product_links,
                    sanitized_category,
                    self.date_stamp,
                    product_url_path,
                )

    def get_product_csv_dict(self, scrape_date=None) -> dict:
        """
         Returns a dictionary that contains file paths to each csv containing product URLs for each store.

        :param scrape_date(str): default is None, which means scrape_date will be derived from current date otherwise a date_stamp string provided will be used (YYYYMMDD)

        returns:
        csv_dict(dict): dictionary that has file paths to each product url csv for each store
        """

        if scrape_date is None:
            scrape_date = self.date_stamp
        else:
            self.date_stamp = scrape_date

        # csv dictionary
        csv_dict = {}

        # define storage path
        for store in self.store_information_dict.keys():
            # get all the csvs for scrape date - if None - get current date
            product_urls_csv_path = (
                self.storage_path
                / f"{store}"
                / f"{scrape_date}"
                / f"{store}_product_urls"
            )

            # create a list to store product csv paths
            product_urls_csv_list = os.listdir(product_urls_csv_path)
            # prepend? the path to the file paths
            product_urls_csv_list = [
                product_urls_csv_path / f"{file_name}"
                for file_name in product_urls_csv_list
            ]

            # add list of csvs to the store key
            csv_dict[store] = product_urls_csv_list

        return csv_dict

    def get_product_data(self, scrape_date=None):
        # call get product csv dict - creates dictionary {store:[list of csvs]}
        product_url_dict = self.get_product_csv_dict(scrape_date)
        # for each store and its list of csvs
        for store, csv_list in product_url_dict.items():
            if store == "Woolworths":
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    # execute get product data from checkers asynchronously
                    results = executor.map(
                        selenium_scrape.get_woolies_product_data, csv_list
                    )
                    # output_list = []
                    # for result in results:
                    #     # convert result iterable to a list - list of product's data from each product in the url
                    #     print(type(result))
                    #     print(result)
                    #     list_result = list(result)
                    #     # add list to output list
                    #     output_list.append(list_result)

            if store == "Checkers":
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    # execute get product data from checkers asynchronously
                    results = executor.map(
                        selenium_scrape.get_checkers_product_data, csv_list
                    )
                    # output_list = []
                    # for result in results:
                    # convert the iterable of product's data to a list
                    # print(type(result))
                    # print(result)
                    # list_result = list(result)
                    # print(list_result)
                    # output_list.append(list_result)

            results = list(np.concatenate(list(results)).flat)
            # create output csv
            product_data_df = pd.DataFrame(results)
            self.store_scraper_logger.info(f"{store} product data frame created.")

            # create path for csv
            save_path = (
                self.storage_path
                / f"{store}"
                / f"{self.date_stamp}"
                / f"{store}_product_data"
                / "raw"
                / f"products_data_{self.date_stamp}.csv"
            )
            # save to csv
            product_data_df.to_csv(
                save_path,
                index=False,
            )

    def process_product_data(self, scrape_date=None) -> None:
        # if scrape_Date argument not given
        if scrape_date is None:
            # use current date
            scrape_date = self.date_stamp
        # otherwise use the given scrape_date
        else:
            self.date_stamp = scrape_date
        # get storage path
        store_paths = [dir for dir in self.storage_path.iterdir() if dir.is_dir()]
        # create processed_data_path list
        raw_file_path_list = []
        # populate list with path to raw files
        for store_path in store_paths:
            raw_file_path_list.append(
                store_path
                / f"{store_path.name}"
                / f"{self.scrape_date}"
                / f"{store_path.name}_product_data"
                / "raw"
                / f"products_data_{self.scrape_date}.csv"
            )
        for raw_file in raw_file_path_list:
            # create data-frame
            df = pd.read_csv(raw_file)
            # drop duplicates
            df = df.drop_duplicates(subset=["barcode"])
            # save file to processed folder
            save_path = (
                raw_file.parent.parent.name
                / "processed"
                / f"products_data_{self.scrape_date}.csv"
            )
            # save file to csv
            df.to_csv(save_path, index=False)

    def upload_products(self, scrape_date=None):

        # if scrape_date argument not given
        if scrape_date is None:
            # use current date
            scrape_date = self.date_stamp
        # otherwise use the given scrape_date
        else:
            self.date_stamp = scrape_date
        # get storage path
        store_paths = [dir for dir in self.storage_path.iterdir() if dir.is_dir()]
        # create processed_data_path list
        processed_file_path_list = []
        # populate list with path to processed files
        for store_path in store_paths:
            processed_file_path_list.append(
                store_path
                / f"{self.scrape_date}"
                / f"{store_path.name}_product_data"
                / "processed"
                / f"processed_products_data_{self.scrape_date}.csv"
            )

        for processed_file in processed_file_path_list:
            database.upload_products(processed_file)
        print("done")
