import logging
import os
import re
from pathlib import Path
import pandas as pd



helper_logger = logging.getLogger("web_scrape.store_scrape")


def create_directory(path) -> None:
    """
    create dictionary to store usrls and logging files
    :param path: directory path to where the files will be stored.
    """
    # convert input string to Path Object
    path = Path(path)
    # check if the folder has already been created
    directory_exits = path.exists()  # os.path.exists(path)

    if directory_exits:
        # print exits - will be removed and replaced with logging
        helper_logger.info(f"{path} exists")
        # print("exists")
    else:
        # if does not exists, create the folder
        path.mkdir()  # os.makedirs(path)
        # print folder created - will be removed
        helper_logger.info(f"{path} created!.")


def get_store_url_dict(spreadsheet_name: str) -> dict:
    """
    Return dictionary that contains product categories as keys and their urls as values.

    :param spreadsheet_name: the path to the csv file that contains category and URL information of each store.

    return:
    category_dict: dictionary containing product categories as keys and their urls.
    """

    # define data path
    file_path = Path(str(Path.cwd()) + f"/data/{spreadsheet_name}")  # r"data//" +

    # load all sheets in the spreadsheet with Pandas
    store_urls_df = pd.read_excel(file_path, sheet_name=None)

    # iterate through each sheet
    for store, store_df in store_urls_df.items():
        # set the categories as the index
        store_df = store_df.set_index("Categories")
        # convert the store_df to dictionary with categories as key and urls as value
        store_df_dict = store_df.to_dict()["URLs"]
        # store each converted dict as value and use the store as a key
        store_urls_df[store] = store_df_dict

    return store_urls_df


def create_product_urls_csv(
    product_urls_list: list, product_category: str, current_date: str, store_path: str
):
    """
    Create a csv file containing product urls.
    :param product_urls_list: a list of product urls scrapped from online store.
    :param product_category: category for which all the product urls belong to
    :param current_date: date when urls were scraped from the internet and saved to the csv
    :param store_path: the path to store the csv

    returns:
    product_urls_csv: csv file containing the product_urls.

    """
    # create a dictionary to store the product urls
    product_dict = {
        "product_urls": product_urls_list,
        "product_category": product_category,
        "product_info_date": current_date,
    }
    # convert a dictionary to pandas dataframe
    product_urls_df = pd.DataFrame(product_dict)

    # write pandas dataframe to a csv
    product_urls_df.to_csv(Path(f"{store_path}/{product_category}.csv"), index=False)
    # give the confirmation product_urls_csv saved
    helper_logger.info(f"{store_path}/{product_category}.csv saved")
    # print(f"{store_path}\\{product_category}.csv saved")


def sanitize_category(raw_category: str) -> str:
    """
    Transforms string to a suitable string that can be used as a file name.

    :param raw_category: string that is not suitable

    return
    clean_category: string that is suitable for use as a category
    """

    # remove white spaces
    white_space_pattern = r"\s"

    clean_category = re.sub(white_space_pattern, "", raw_category)

    # define unwanted characters
    unwanted_characters = "[&,]"

    clean_category = re.sub(unwanted_characters, "_", clean_category)

    return clean_category


def get_weight_components(weight_string: str) -> list:
    """
    Get the weight information from the product string - information
    number items, product weight per item, units

    :param weight_string (str): product name collected from product page.

    returns
    product_name_split (list): contains product weight information
    """
    # combination regular expression pattern
    combination_weight_patterns = [
        "[0-9]+ x [0-9]+ x [0-9]+(g|kg|ml|L)",  # 6 x 6 x 12ml
        "[0-9]+ x [0-9]+ (g|kg|ml|L)",  # 12 x 750 ml
        "[0-9]+ x [0-9]+.[0-9]+ (g|kg|ml|L)",  # 6 x 75.52 ml
        "[0-9]+x[0-9]+.[0-9]+ (g|kg|ml|L)",  # 27x15.5 L
        "[0-9]+x[0-9]+(g|kg|ml|L)",  # 24x250ml
        "[0-9]+ x [0-9]+(g|kg|ml|L)",  # 24 x 355ml
        "[0-9]+ x [0-9]+.[0-9]+(g|kg|ml|L)",  # 6 x 75.52ml
    ]
    # singular regular expression pattern
    singular_weight_patterns = [
        "[0-9]+ (g|kg|ml|L)",  # 150 ml
        "[0-9]+(g|kg|ml|L)",  # 150ml
        "[0-9]+.[0-9]+ (g|kg|ml|L)",  # 1.5 ml
        "[0-9]+.[0-9]+(g|kg|ml|L)",  # 47.5ml
    ]
    # search through the combination product weight pattern
    combination_weight_search = re.search(
        "|".join(combination_weight_patterns), weight_string
    )
    singular_weight_search = re.search(
        "|".join(singular_weight_patterns), weight_string
    )
    # check if product name contains a combination_weight string pattern
    if combination_weight_search:
        # if it does, split the sting into components - list
        product_name_split = combination_weight_search.group().split(" x ")
    # check if the product name contains a singular_weight string pattern
    elif singular_weight_search:
        # if it does, split the string into components - list
        product_name_split = singular_weight_search.group().split(" x ")
    else:
        # return None
        product_name_split = None

    return product_name_split if product_name_split else None


def get_weight_unit(weight_unit_string: str) -> str:
    """
    Returns the unit of the product if it can be converted to kilogrammes.
    Parameters:
    :param weight_unit_string (str): string that should contain a products weight value and unit.

    Returns
    str: returns a product's unit of weight.
    """
    unit_pattern_dict = {
        "grammes_pattern": "\sg|g",
        "kilogrammes_pattern": "\skg|kg",
        "mill_litres_pattern": "\sml|ml",
        "litres_pattern": "\sL|L",
    }
    # check if the weight_unit string has a grammes pattern
    if re.search(unit_pattern_dict["kilogrammes_pattern"], weight_unit_string) != None:
        # return the weight unit as a string
        return (
            re.search(unit_pattern_dict["kilogrammes_pattern"], weight_unit_string)
            .group()
            .strip()
        )
    # check if the weight_unit string has a kilogrames pattern
    elif re.search(unit_pattern_dict["grammes_pattern"], weight_unit_string) != None:
        # return the kg unit as string
        return (
            re.search(unit_pattern_dict["grammes_pattern"], weight_unit_string)
            .group()
            .strip()
        )
    # check if the weight_unit string has a millilitres pattern
    elif (
        re.search(unit_pattern_dict["mill_litres_pattern"], weight_unit_string) != None
    ):
        # return the ml unit as string
        return (
            re.search(unit_pattern_dict["mill_litres_pattern"], weight_unit_string)
            .group()
            .strip()
        )
    # check if the weight_unit string has a Litres pattern
    elif re.search(unit_pattern_dict["litres_pattern"], weight_unit_string) != None:
        # return the L unit as string
        return (
            re.search(unit_pattern_dict["litres_pattern"], weight_unit_string)
            .group()
            .strip()
        )
    else:
        return None


def get_product_weight(product_name_string: str) -> float:
    """
    Calculates the weight of a product using the product name string.

    :parma product_name_string(str): this is the name of the product contains product weight

    returns
    product_weight(float) - weight of the product in kilogrammes
    """
    # get the weight components
    weight_components_list = get_weight_components(product_name_string)
    # check if singular or combination weight pattern

    # get the number of elements in the list  - 1-singular,  > 1 combination
    # if weight_list is not None
    if weight_components_list != None:
        # get the number of elements in the list
        num_components = len(weight_components_list)
    # else is None
    else:
        # return None
        return None
    # check if there is only one item in the list - singular weight pattern
    if num_components == 1:
        # extract product unit of weight - kg, g, ml, L
        product_unit_weight = get_weight_unit(weight_components_list[-1])
        # check if unit weight is grammes (g) or millilitres (ml)
        if product_unit_weight == "g" or product_unit_weight == "ml":
            # attempt to convert weight to float
            try:
                # select the item in list, replace unit, convert value float then divide by 1000
                product_weight = (
                    float(weight_components_list[-1].replace(product_unit_weight, ""))
                    / 1000
                )
            # could not convert to float
            except Exception as error:
                # set product weight to error
                product_weight = "error"
        # if not grammes or millilitres, then it is litres and kilogrammes no need to divide by 1000
        else:
            try:
                product_weight = float(
                    weight_components_list[-1].replace(product_unit_weight, "")
                )
            except Exception as error:
                product_weight = "error"
    # num components is greater than 1 - combination weight pattern
    else:
        # get unit weight from weight components list - always the last
        product_unit_weight = get_weight_unit(weight_components_list[-1])
        # check if it is grammes (g) or millilitres (ml)
        if product_unit_weight == "g" or product_unit_weight == "ml":
            try:

                product_base_weight = (
                    float(weight_components_list[-1].replace(product_unit_weight, ""))
                    / 1000
                )
            except Exception as error:
                product_base_weight = "error"
        # not grammes or millilitres - L or kg
        else:
            try:
                product_base_weight = float(
                    weight_components_list[-1].replace(product_unit_weight, "")
                )
            except Exception as error:
                product_base_weight = "error"
        if product_base_weight != "error":
            if num_components == 2:
                product_weight = float(weight_components_list[0]) * product_base_weight
            elif num_components == 3:
                product_weight = (
                    float(weight_components_list[0])
                    * float(weight_components_list[1])
                    * product_base_weight
                )
        else:
            product_weight = product_base_weight

    if isinstance(product_weight, str):
        return "error"
    else:
        product_weight_final = round(product_weight, 2)
        helper_logger.info(f"{product_name_string} -- weight: {product_weight_final}")
        return product_weight_final


# def weight_extract_convert(weight_string: str) -> str:
#     """
#     Uses regular expressions to extract and convert the weight of the product.

#     :param weight_string (str): a the product name contains the weight of the product

#     return:
#     product_weight(str): product_weight
#     """

#     # combination product weight pattern
#     # 12 x 100 L
#     # 6 x 12.05 kg
#     combination_weight_re = "[0-9]+ x [0-9]+ (g|kg|ml|L)|[0-9]+ x [0-9]+.[0-9]+ (g|kg|ml|L)|[0-9]+x[0-9]+.[0-9]+ (g|kg|ml|L)|[0-9]+x[0-9]+(g|kg|ml|L)"

#     # singular product weight pattern
#     singular_weight_re = "[0-9]+ (g|kg|ml|L)|[0-9]+(g|kg|ml|L)"

#     # check for combination string
#     if re.search(combination_weight_re, weight_string):
#         # split the string into list - [num units, weight_per_unit]
#         combination_split = (
#             re.search(combination_weight_re, weight_string).group().split(" x ")
#         )

#         # num units
#         num_units = int(combination_split[0])
#         # unit_string -[g,kg,ml,L]
#         weight_unit_string = combination_split[1]

#         # check if weight unit is grammes
#         if " g" in weight_unit_string:
#             # remove the gramme unit, convert string to float
#             weight = float(weight_unit_string.replace(" g", ""))
#             # divide weight by 1000 to convert to kg
#             weight = weight / 1000 * num_units
#         # check if weight units is ml
#         elif " ml" in weight_unit_string:
#             # remove the ml unit, convert string to float
#             weight = float(weight_unit_string.replace(" ml", ""))
#             # divide weight by 1000 to convert to kg
#             weight = weight / 1000 * num_units
#         # check if kg unit in string
#         elif " kg" in weight_unit_string:
#             # remove the kg unit, convert string to float
#             weight = float(weight_unit_string.replace(" kg", "")) * num_units
#         else:
#             # remove L unit in string, convert string to float
#             weight = float(weight_unit_string.replace(" L", "")) * num_units
#     elif re.search(singular_weight_re, weight_string):
#         # singular algorithm
#         weight_string_singular = re.search(singular_weight_re, weight_string).group()
#         if " g" in weight_string_singular:
#             weight = float(weight_string_singular.replace(" g", "")) / 1000
#         elif " ml" in weight_string_singular:
#             weight = float(weight_string_singular.replace(" ml", "")) / 1000
#         elif " kg" in weight_string_singular:
#             weight = float(weight_string_singular.replace(" kg", ""))
#         else:
#             weight = float(weight_string_singular.replace(" L", ""))
#     else:
#         weight = None
#     try:
#         return round(weight, 2)
#     except:
#         return None
