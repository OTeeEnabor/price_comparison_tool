import os
from pathlib import Path
import sys

import pandas as pd
import numpy as np

# append project directory
sys.path.append(
    str(Path.cwd())#"C:\\Users\\user\\Documents\\Open Delta Youtube\\Python\\price_comparison_tool"
)
import web_scrape.helpers

# get the path to data file
store_list = ["Checkers", "Woolworths"]
date_stamp = "20240712"
for store in store_list:
    # get data file
    data_filepath = Path.cwd() / "data" / "stores" / f"{store}" / f"{date_stamp}" / f"{store}_product_data"/"raw" / f"products_data_{date_stamp}.csv"
    # create pandas data frame
    df_raw = pd.read_csv(data_filepath)
    # show the first 5 observations
    df_raw.head()
    # show shape information
    print(f"{store} Information")
    print("*"*25)
    # number of rows
    no_rows = df_raw.shape[0]
    # get the total number rows that have null values
    print(df_raw.isnull().sum())
    total_null = df_raw.isnull().sum().sum()
    print(total_null)
    null_ratio = f"{(total_null/no_rows):.2f}"
    info_string = f"{store} - data scrapped on {date_stamp} has a null ratio of - {null_ratio}"
    print(info_string)
    print("*"*25)
# # make a copy of the data frame
# df_copy = df_raw.copy()

# # get the product_weight column
# product_weight_series = df_copy["weight"]

# # group series by its values - excludes NaN
# product_weight_series_count = product_weight_series.value_counts()

# # apply the helpers.get_weight function to the series
# # get product_name
# product_name_series = df_copy["name"]
# # web_scrape.helpers.get_product_weight()

# product_weight_series_ = product_name_series.apply(lambda x: web_scrape.helpers.get_product_weight(x) if isinstance(x,str) else x)

# product_weight_series_.value_counts()
# product_weight_series_.filter(items=["error"])
# error_list = []
# for name in product_name_series:
#     print(f"Product name {name}\n")
#     try:

#         weight = web_scrape.helpers.get_product_weight(name)
#     except Exception as error:
#         error_list.append(name)
#     else:
#         print(f"Product weight: {weight}")
#     print("*" * 25)

# print(len(error_list))

# edge_1 = error_list[0]
# split_by_x = web_scrape.helpers.get_weight_components(edge_1)[0].split("x")
# print(split_by_x)

# df_copy["weight"] = product_weight_series_
# df_copy.head()
# df_copy.to_csv(os.getcwd()
#     + r"\data\stores\Checkers\2024612\Checkers_product_data\products_data_2024612_.csv", index=False)