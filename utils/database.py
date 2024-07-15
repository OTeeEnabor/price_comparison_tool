"""
-- connect to the database
-- get the data
-- upload the data 
-- end connection
"""
import csv
import sys
from pathlib import Path

# append project directory - change to cwd
PROJECT_PATH = Path.cwd()

sys.path.append(str(PROJECT_PATH))


from config.config_ import load_config
from config.connect import connect

# FILE_PATH = Path.cwd()/"data"/"stores"/"Woolworths"/"2024626"/"Woolworths_product_data"/"products_data_2024626.csv"

def upload_products(file_path:Path):

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

    with open(file_path,'r') as file:
        # create csv reader
        reader = csv.reader(file)
        # skip the header
        next(reader)

        for row in reader:
            cur.execute(insert_statement, row)
    # commit transaction
    conn.commit()
    # close the cursor
    cur.close()
    # close the connection
    conn.close()
        
