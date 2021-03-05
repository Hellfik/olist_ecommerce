import sqlite3


DB_NAME = 'olist_db.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()


# Initialisation du dictionnaire de tables

TABLES = {}

TABLES['olist_customers_dataset'] = (
    '''CREATE TABLE olist_customers_dataset (
        customer_id char(32) NOT NULL,
        customer_unique_id char(32),
        customer_zip_code char(5),
        customer_state char(2),
        PRIMARY KEY (customer_id),
        FOREIGN KEY (customer_zip_code)
            REFERENCES olist_geolocation_dataset(geolocation_zip_code_prefix)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        )''' )

TABLES['olist_orders_dataset'] = (
    '''CREATE TABLE olist_orders_dataset (
        order_id char(32) NOT NULL,
        customer_id char(32),
        order_status varchar(20),
        order_purchase_timestamp datetime,
        order_approved_at datetime,
        order_delivered_carrier_date datetime,
        order_estimated_customer_date datetime,
        order_estimated_delivery_date datetime,
        PRIMARY KEY (order_id),
        FOREIGN KEY (customer_id)
            REFERENCES customers_dataset(customer_id)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        )''' )

TABLES['olist_geolocation_dataset'] = (
    '''CREATE TABLE olist_geolocation_dataset (
        geolocation_zip_code_prefix mediumint NOT NULL,
        geolocation_lat decimal(16,14),
        geolocation_lng decimal(16,14),
        geolocation_city varchar(30),
        geolocation_state char(2)
        )''' )

TABLES['olist_order_items_dataset'] = (
    '''CREATE TABLE olist_order_items_dataset (
        order_id char(32) NOT NULL,
        order_item_id char(32) NOT NULL,
        product_id char(32) NOT NULL,
        seller_id char(32) NOT NULL,
        shipping_limit_date datetime,
        price DECIMAL(9,2) NOT NULL,
        freight_value DECIMAL (8,2),
        PRIMARY KEY (order_id),
        FOREIGN KEY (product_id)
            REFERENCES olist_products_dataset(product_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY (seller_id)
            REFERENCES olist_sellers_dataset(seller_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )''' )

TABLES['olist_order_payments_dataset'] = (
    '''CREATE TABLE olist_order_payments_dataset (
        id,
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value
        )''' )

TABLES['olist_order_reviews_dataset'] = (
    '''CREATE TABLE olist_order_reviews_dataset (
        review_id char(32),
        order_id char(32),
        review_score tinyint,
        review_comment_title varchar(50),
        review_comment_message varchar(250),
        review_creation_date datetime,
        review_answer_timestamp datetime,
        PRIMARY KEY (review_id),
        FOREIGN KEY (order_id)
            REFERENCES olist_orders_dataset(order_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        )''' )

TABLES['olist_products_dataset'] = (
    '''CREATE TABLE olist_products_dataset (
        product_id char(32),
        product_category_name varchar(30),
        product_name_length tinyint,
        product_description_length smallint,
        product_photo_qty tinyint,
        product_weight_g smallint,
        product_length_cm tinyint,
        product_height_cm tinyint,
        product_width_cm tinyint,
        PRIMARY KEY (product_id),
        FOREIGN KEY (product_category_name)
            REFERENCES product_category_name_translation(product_category_name_english)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        )''' )

TABLES['olist_sellers_dataset'] = (
    '''CREATE TABLE olist_sellers_dataset (
        seller_id char(32),
        seller_zip_code_prefix char(5),
        seller_city varchar(30),
        seller_state char(2),
        PRIMARY KEY (seller_id),
        FOREIGN KEY (seller_zip_code_prefix)
            REFERENCES olist_geolocation_dataset(geolocation_zip_code_prefix)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        )''' )
    
TABLES['product_category_name_translation'] = (
    '''CREATE TABLE product_category_name_translation (
        product_category_name varchar(30),
        product_category_name_english varchar(30),
        PRIMARY KEY (product_category_name)
        )''' )



# Créer les tables du dictionnaire TABLES

for table_name in TABLES:
    table_description = TABLES[table_name]
    print("Creating table {}: \n".format(table_name), end='')
    cur.execute(table_description)





# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()



