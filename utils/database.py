"""
-- connect to the database
-- get the data
-- upload the data 
-- end connection
"""

import csv
import sys
from pathlib import Path

import numpy as np

# append project directory - change to cwd
PROJECT_PATH = Path.cwd()

sys.path.append(str(PROJECT_PATH))


from config.config_ import load_config
from config.connect import connect


# FILE_PATH = Path.cwd()/"data"/"stores"/"Woolworths"/"2024626"/"Woolworths_product_data"/"products_data_2024626.csv"
def set_none_values(input):
    """
    This function removes empty strings (none values) with None.
    """
    if input == "" or input == "error":
        return np.nan
    else:
        return input


def upload_products(file_path: Path):

    # load database configurations
    config = load_config()

    # connect to database
    conn = connect(config)

    # load the data
    # category,date,name,barcode,price,weight,url,store
    insert_statement = """
    INSERT INTO products(product_category, product_date, product_name,
                        product_barcode, product_price, product_weight, 
                        product_url, product_store)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """
    # create cursor
    cur = conn.cursor()

    with open(file_path, "r") as file:
        # create csv reader
        reader = csv.reader(file)
        # skip the header
        next(reader)

        for row in reader:
            # create numpy array
            row_array = np.array(row)
            # apply vectorized processing
            vectorized_process = np.vectorize(set_none_values)
            # pass array to vectorised function
            row_array_processed = vectorized_process(row_array)
            # for i, item in enumerate(row):
            #     if item == "" or item=="error":
            #         row[i] = None
            cur.execute(insert_statement, row_array_processed)
    # commit transaction
    conn.commit()
    # close the cursor
    cur.close()
    # close the connection
    conn.close()
