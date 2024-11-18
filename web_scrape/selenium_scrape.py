import logging
import time
import os
from datetime import date
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException

from . import helpers

# get logger - store scrape
sel_scraper_logger = logging.getLogger("web_scrape.store_scrape")


def extract_number_from_string(string):
    """
    extracts the number from a string
    """
    # re number pattern
    number_re_pattern = "[0-9]+"
    match_object = re.search(number_re_pattern, string)
    if match_object:
        return int(match_object.group())


def create_driver():
    """
    returns a Selenium ChromeWebdriver instance to automate scraping process.

    returns:
    WebDriver object
    """
    # initialise the webdriver options
    options = webdriver.ChromeOptions()
    # set the mode - options for the webdriver using Service object
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    # define the path of the driver
    DRIVER_PATH = Path(str(Path.cwd()) + r"/web_scrape/chromedriver.exe")
    # define the service object
    serv_obj = Service(DRIVER_PATH, service_args=["--log-level=INFO"])
    # create selenium driver
    driver = webdriver.Chrome(service=serv_obj, options=options)
    return driver


def click_next_page_button_checkers(driver):
    """
    Clicks on the next page button on Checkers online store.
    :param driver: This is an instance of a ChromeWebDriver class.
    Returns
    None
    """
    # find the next page button
    next_page_button_checkers = driver.find_elements(By.CLASS_NAME, "pagination-next")[
        0
    ]
    next_page_button_checkers = next_page_button_checkers.find_elements(
        By.XPATH, ("*")
    )[0]

    wait = WebDriverWait(driver, 5)

    next_page_button_checkers = wait.until(EC.visibility_of(next_page_button_checkers))

    # click on the next page button
    try:
        next_page_button_checkers.click()
    except Exception as error:
        sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # refresh the page
        driver.refresh()
        # try to call the function again - possible to enter infinite loop
        click_next_page_button_checkers(driver)


def get_checkers_price(soup_price_string):
    if "," not in soup_price_string:
        product_price = soup_price_string.replace("R", "")
    else:
        product_price = soup_price_string.replace(",", "")
        product_price = product_price.replace("R", "")
    return float(product_price)

    # page_soup.css.select(f".prod--price")[0].get_text()
    # product_price = float(
    #             page_soup.css.select(f".prod--price")[0].get_text().replace("R ", "")
    #         )


def get_woolworth_urls(driver) -> list:
    """
    get list of product urls from woolworths online store
    :param driver: Selenium WebDriver instance
    returns:
    product_link_list: list of product urls found in this category
    """
    # try to find the number of items in this category
    try:
        product_count_str = driver.find_element(
            By.CLASS_NAME, "product-records__count"
        ).text
    except Exception as error:
        sel_scraper_logger.info("Error occurred while trying to find the number of items on this page")
        sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # print(f"An unexpected error occurred attempting to get product-count string - {error}")
    else:
        product_count_int = extract_number_from_string(product_count_str)
        # print("*" * 25)
        sel_scraper_logger.info(
            f"The number of products found for this category - {product_count_int}"
        )
        # print(f"The number of products found for this category - {product_count_int}")
        # print("*" * 25)

        if product_count_int == None:
            product_count_int = 500

    # find the next page button
    try:
        next_page_button_woolworths = driver.find_elements(
            By.CLASS_NAME, "pagination__nav"
        )[1]
    except IndexError as error:
        sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        next_page_button_woolworths = driver.find_elements(
            By.CLASS_NAME, "pagination__nav"
        )[0]
    except Exception as error:
        sel_scraper_logger.exception(error, stack_info=True, exc_info=True)

    # initialise the page counter
    page_counter = 1
    # check if the next page button is displayed
    if next_page_button_woolworths.is_displayed():
        sel_scraper_logger.info("Woolworths next page button found")
        # sleep for 5 seconds
        # time.sleep(5)
        # create an empty list to store product links
        product_link_list = []

        while True:
            # try to remove the cookie modal from DOM usingJS
            try:
                cookie_div = driver.find_element(By.ID,"cookie-root")
            except NoSuchElementException as error:
                 # inform number of products scraped
                sel_scraper_logger.info(
                    f"Woolworths - no cookie html banner to remove"
                )
                cookie_div = False
                
            if cookie_div:
                driver.execute_script("document.getElementById('cookie-root').remove();")
                 # inform number of products scraped
                sel_scraper_logger.info(
                    f"Woolworths - cookie html banner removed."
                )
            try:
                # find all anchor tags with the class - product--view
                product_anchors = driver.find_elements(By.CLASS_NAME, "product--view")
            except Exception as error:
                sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
            else:
                for anchor in product_anchors:
                    # get the url
                    product_link = anchor.get_attribute("href")
                    # append product link to the list of product links
                    product_link_list.append(product_link)
            # inform number of products scraped
            sel_scraper_logger.info(
                f"{len(product_anchors)} products scraped on page - {page_counter}"
            )
            # inform number of products scraped in total
            sel_scraper_logger.info(
                f"Number of products scrapped so far - {len(product_link_list)}"
            )

            # find the next_page_button again
            next_page_button_woolworths = driver.find_elements(
                By.CLASS_NAME, "pagination__nav"
            )

            # check if there is more than one button found
            if len(next_page_button_woolworths) > 1:
                next_page_button_woolworths = next_page_button_woolworths[1]

            # check if the number of products scrapped is larger than the product count
            if len(product_link_list) > product_count_int:
                sel_scraper_logger.info("Collected more products than on category")
                break
            # try to click on the next page button
            else:

                try:
                    # click on button
                    next_page_button_woolworths.click()
                except ElementNotInteractableException as error:
                    sel_scraper_logger.exception(error)
                except Exception as error:
                    sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
                    break

            # increment page counter
            page_counter += 1
            sel_scraper_logger.info(
                f"Woolworth next page button clicked - going to page - {page_counter}"
            )
            driver.implicitly_wait(10)

    return product_link_list


def get_checkers_urls(driver):
    """
    Returns a list of product urls in a food category.

    :param driver (WebDriver): This is an instance of a ChromeWebDriver class.
    return
    product_link_list (list): returns a list of product links.
    """

    # set the next page button
    next_page_button_checkers = driver.find_elements(By.CLASS_NAME, "pagination-next")[
        0
    ].find_elements(By.XPATH, ("*"))[0]

    # check button is displayed
    if next_page_button_checkers.is_displayed():
        # kill the script for 2 seconds
        # time.sleep(2)
        # create list to store product links
        product_link_list = []
        #  loop through all the pages in this category
        while True:
            try:
                # get all the elements that are products using the css class selector below
                products = driver.find_elements(By.CLASS_NAME, "item-product__image")
                # get the anchor tags
                product_anchors = [
                    product.find_elements(By.XPATH, "*")[0] for product in products
                ]
                sel_scraper_logger.info(
                    f"{len(product_anchors)} product urls collected. "
                )
            except Exception as error:
                sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
                break
            # iterate through each anchor
            for product_anchor in product_anchors:
                # try to get the link for each product_anchor
                try:
                    # get href attribute for each product_anchor
                    product_link = product_anchor.get_attribute("href")
                    # append to the list
                    product_link_list.append(product_link)
                except Exception as error:
                    sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
            try:
                # find the next page disabled element
                next_page_button_checkers_disabled = driver.find_elements(
                    By.CSS_SELECTOR, ".pagination-next.disabled"
                )
            except Exception as error:
                sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
                break
            else:
                if next_page_button_checkers_disabled:
                    break
                else:
                    click_next_page_button_checkers(driver)
    return product_link_list


def url_scraper(category_url: str, store: str) -> list:
    """
    Returns a list of URLS collected from a product category page.

    :param category_url (str): the product category page URL
    :param store(str): determines which scraping logic function should be executed.

    return
    product_link_list (list): list of urls collected from the category page
    """

    # instantiate a selenium web driver with the service object
    driver = create_driver()

    # implicit wait
    driver.implicitly_wait(0.5)
    # maximise the browser window
    driver.maximize_window()
    # get the html of the category url
    driver.get(category_url)
    # wait for 5 seconds to load
    # time.sleep(5)

    # look for each product URL in this category
    if store == "Woolworths":
        product_urls_list = get_woolworth_urls(driver)
    elif store == "Checkers":
        pass
        product_urls_list = get_checkers_urls(driver)
    
    # quit the driver
    driver.quit()

    return product_urls_list


def get_woolies_product_data(csv_file_path: str) -> list:
    """
    Collect data from the scraped product urls

    :param csv_file_path(str): file path to product urls csv

    returns
    output_list_dicts (list): list of dictionaries containing product data
    """
    # initialise driver object
    sel_driver = create_driver()
    # try to read product urls csv
    try:
        # create product urls dataframe from csv file
        product_df = pd.read_csv(csv_file_path)
    # if any exception occurs
    except Exception as error:
        # log exception and move on
        sel_scraper_logger.exception(error, stack_info=True, exc_info=True)

    # define output list to store dictionaries
    output_list_dicts = []
    # get the product category
    product_category = product_df["product_category"][0]
    # get the information date
    product_info_date = product_df["product_info_date"][0]
    # loop through the product_urls to scrape product data
    for product_link in product_df["product_urls"]:
        # create the product dictionary
        product_dict = {}
        # set the product category
        product_dict["category"] = product_category
        # set the date of product information - date collected
        product_dict["date"] = product_info_date
        # scrape with beautiful soup
        try:
            # get the web page
            sel_driver.get(product_link)
            # parse the web page with beautiful soup
            page_soup = BeautifulSoup(sel_driver.page_source, "html.parser")
        except Exception as error:
            # log the error
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
            # skip the current iteration and proceed to the next
            continue
        # try to get the product name
        try:
            # get the product name
            product_name = page_soup.css.select(".prod-name")[0].get_text()
        except Exception as error:
            product_name = None
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # try to get the product barcode
        try:
            product_barcode = (
                page_soup.find("li", string="Product code:")
                .find_next_sibling()
                .get_text()
            )
        except Exception as error:
            product_barcode = None
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # try to get the product price
        try:
            product_price = float(
                page_soup.css.select(f".prod--price")[0].get_text().replace("R ", "")
            )
        except Exception as error:
            product_price = None
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # if product name successfully collected
        if product_name != None:
            try:
                # get the weight
                product_weight = helpers.get_product_weight(product_name)
            except Exception as error:
                product_weight = None
                sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # error in product name - set product weight to None
        else:
            product_weight = None

        # selected product information to product dictionary
        product_dict["name"] = product_name
        product_dict["barcode"] = product_barcode
        product_dict["price"] = product_price
        product_dict["weight"] = product_weight
        product_dict["url"] = product_link
        product_dict["store"] = "Woolworths"

        # append to the output list
        output_list_dicts.append(product_dict)
        sel_scraper_logger.info(f"completed scraping -- {product_link}")
    # return the list of dictionaries
    return output_list_dicts


def get_checkers_product_data(csv_file_path: str) -> list:
    """
    Returns a list of dictionaries containing product information from all the products in the csv.

    :param csv_file_path: the file path to the csv that contains product urls.

    returns:
    output_list_dicts: returns a list of dictionaries.

    """
    # initialise driver object
    sel_driver = create_driver()
    try:
        product_df = pd.read_csv(csv_file_path)
    except Exception as error:
        sel_scraper_logger.exception(error, stack_info=True, exc_info=True)

    # define output list to store dictionaries
    output_list_dicts = []
    # get the product category
    product_category = product_df["product_category"][0]
    # get the product information date
    product_info_date = product_df["product_info_date"][0]
    # loop through the product_urls to scrape products
    for product_link in product_df["product_urls"]:

        # create the product dictionary
        product_dict = {}
        # set product category
        product_dict["category"] = product_category
        # set the date of product information
        product_dict["date"] = product_info_date
        # try to scrape with beautiful soup
        try:
            # get the web page
            sel_driver.get(product_link)
            # parse the web page with beautiful soup with html parser
            page_soup = BeautifulSoup(sel_driver.page_source, "html.parser")
        except Exception as error:
            # log the error
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
            # skip this current iteration and proceed with the next
            continue
        # try to get the product name
        try:
            # get the product name
            product_name = page_soup.css.select(".pdp__name")[0].get_text()
        except Exception as error:
            product_name = None
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # try to get the product barcode
        try:
            product_barcode = page_soup.css.select(".pdp__id")[0].getText()
        except Exception as error:
            product_barcode = None
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # if product barcode successfully selected
        else:
            # extract number from string
            number_re_pattern = "[0-9]+"
            match_object = re.search(number_re_pattern, product_barcode)
            # if a match exists
            if match_object:
                # extract the barcode
                product_barcode = match_object.group()
            # if match doesn't exist - set to None
            else:
                product_barcode = None
        # try to get the product price
        try:
            # get the product price
            product_price = page_soup.css.select(".special-price__price")[0].getText()
            product_price = get_checkers_price(product_price)
        except Exception as error:
            product_price = None
            sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # if the product name is not None
        if product_name != None:
            # try to get the product weight
            try:
                # get the product weight
                product_weight = helpers.get_product_weight(product_name)
            except Exception as error:
                product_weight = None
                sel_scraper_logger.exception(error, stack_info=True, exc_info=True)
        # if product name is None - set product weight to None
        else:
            product_weight = None
        # add product information to product dictionary
        product_dict["name"] = product_name
        product_dict["barcode"] = product_barcode
        product_dict["price"] = product_price
        product_dict["weight"] = product_weight
        product_dict["category"] = product_category
        product_dict["url"] = product_link
        product_dict["store"] = "Checkers"

        # append to list
        output_list_dicts.append(product_dict)
        sel_scraper_logger.info(
            f"completed scraping Checkers product data --- {product_link}"
        )
    # return list of dictionaries
    return output_list_dicts
