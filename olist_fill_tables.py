import sqlite3
import pandas as pd

DB_NAME = 'olist_db.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute('pragma encoding=UTF8')

"""
CUSTOMERS DATAFRAME + WRITE INTO SQLITE TABLE

"""

customers_dataset = pd.read_csv('datasets/olist_customers_dataset.csv')

customers_df = pd.DataFrame(customers_dataset)

customers_dataset.to_sql(
    name="olist_customers_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)


"""
GEOLOCATION DATAFRAME + WRITE INTO SQLITE TABLE

"""

geolocation_dataset = pd.read_csv('datasets/olist_geolocation_dataset.csv')

geolocation_df = pd.DataFrame(geolocation_dataset)

geolocation_dataset.drop_duplicates(subset=['geolocation_zip_code_prefix']).to_sql(
    name="olist_geolocation_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)

"""
BASKET DATAFRAME + WRITE INTO SQLITE TABLE

"""

order_list_items_dataset = pd.read_csv('datasets/olist_order_items_dataset.csv')

order_list_items_df = pd.DataFrame(order_list_items_dataset)


order_list_items_df.drop_duplicates(subset=['order_id']).to_sql(
    name="olist_order_items_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)

"""
ORDER PAYMENTS DATAFRAME + WRITE INTO SQLITE TABLE

"""

order_payments_dataset = pd.read_csv('datasets/olist_order_payments_dataset.csv')
order_payments_df = pd.DataFrame(order_payments_dataset)

order_payments_df.to_sql(
    name="olist_order_payments_dataset",
    con=con,
    index=True,
    if_exists='replace',
    chunksize=500
)

"""
REVIEWS DATAFRAME + WRITE INTO SQLITE TABLE

"""

order_reviews_dataset = pd.read_csv('datasets/olist_order_reviews_dataset.csv')
order_reviews_df = pd.DataFrame(order_reviews_dataset)

order_reviews_df.drop_duplicates(subset=['review_id']).to_sql(
    name="olist_order_reviews_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)

"""
ORDERS DATAFRAME + WRITE INTO SQLITE TABLE

"""

orders_dataset = pd.read_csv('datasets/olist_orders_dataset.csv')
order_df = pd.DataFrame(orders_dataset)

order_df.to_sql(
    name="olist_orders_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)

"""
PRODUCTS DATAFRAME + WRITE INTO SQLITE TABLE

"""

products_dataset = pd.read_csv('datasets/olist_products_dataset.csv')
products_df = pd.DataFrame(products_dataset)

products_df.to_sql(
    name="olist_products_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)

"""
SELLERS DATAFRAME + WRITE INTO SQLITE TABLE

"""

sellers_dataset = pd.read_csv('datasets/olist_sellers_dataset.csv')
sellers_df = pd.DataFrame(sellers_dataset)

sellers_df.to_sql(
    name="olist_sellers_dataset",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)

"""
PRODUCT NAME CATEGORY DATAFRAME + WRITE INTO SQLITE TABLE

"""

product_name_dataset = pd.read_csv('datasets/product_category_name_translation.csv')
product_name_df = pd.DataFrame(product_name_dataset)

product_name_df.to_sql(
    name="product_category_name_translation",
    con=con,
    index=False,
    if_exists='replace',
    chunksize=500
)


