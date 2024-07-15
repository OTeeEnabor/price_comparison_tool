import os
import sys

import pandas as pd
import numpy as np

# append project directory
sys.path.append(
    "C:\\Users\\user\\Documents\\Open Delta Youtube\\Python\\price_comparison_tool"
)
import web_scrape.helpers

# get the path to data file
data_filepath = (
    os.getcwd()
    + r"\data\stores\Checkers\2024612\Checkers_product_data\products_data_2024612.csv"
)

# create pandas data frame
df_raw = pd.read_csv(data_filepath)

# show the first 5 observations
df_raw.head()

# make a copy of the data frame
df_copy = df_raw.copy()

# get the product_weight column
product_weight_series = df_copy["weight"]

# group series by its values - excludes NaN
product_weight_series_count = product_weight_series.value_counts()

# apply the helpers.get_weight function to the series
# get product_name
product_name_series = df_copy["name"]
# web_scrape.helpers.get_product_weight()

product_weight_series_ = product_name_series.apply(lambda x: web_scrape.helpers.get_product_weight(x) if isinstance(x,str) else x)

product_weight_series_.value_counts()
product_weight_series_.filter(items=["error"])
error_list = []
for name in product_name_series:
    print(f"Product name {name}\n")
    try:

        weight = web_scrape.helpers.get_product_weight(name)
    except Exception as error:
        error_list.append(name)
    else:
        print(f"Product weight: {weight}")
    print("*" * 25)

print(len(error_list))

edge_1 = error_list[0]
split_by_x = web_scrape.helpers.get_weight_components(edge_1)[0].split("x")
print(split_by_x)

df_copy["weight"] = product_weight_series_
df_copy.head()
df_copy.to_csv(os.getcwd()
    + r"\data\stores\Checkers\2024612\Checkers_product_data\products_data_2024612_.csv", index=False)