import pandas as pd
from sqlalchemy import create_engine, text

# =========================
# DATABASE CONNECTION
# =========================

engine = create_engine(
    "postgresql+psycopg2://postgres:12344321@localhost:5432/ecommerce"
)

# =========================
# CREATE TABLES
# =========================

with engine.connect() as conn:
    conn.execute(text("""

    DROP TABLE IF EXISTS order_reviews;
    DROP TABLE IF EXISTS payments;
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS sellers;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        customer_id TEXT PRIMARY KEY,
        customer_unique_id TEXT,
        customer_zip_code_prefix INT,
        customer_city TEXT,
        customer_state TEXT
    );

    CREATE TABLE sellers (
        seller_id TEXT PRIMARY KEY,
        seller_zip_code_prefix INT,
        seller_city TEXT,
        seller_state TEXT
    );

    CREATE TABLE orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_status TEXT,
        order_purchase_timestamp TIMESTAMP,
        order_approved_at TIMESTAMP,
        order_delivered_carrier_date TIMESTAMP,
        order_delivered_customer_date TIMESTAMP,
        order_estimated_delivery_date TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE products (
        product_id TEXT PRIMARY KEY,
        product_category_name TEXT,
        product_name_lenght INT,
        product_description_lenght INT,
        product_photos_qty INT,
        product_weight_g REAL,
        product_length_cm REAL,
        product_height_cm REAL,
        product_width_cm REAL
    );

    CREATE TABLE order_items (
        order_id TEXT,
        order_item_id INT,
        product_id TEXT,
        seller_id TEXT,
        shipping_limit_date TIMESTAMP,
        price REAL,
        freight_value REAL,
        PRIMARY KEY (order_id, order_item_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
    );

    CREATE TABLE payments (
        order_id TEXT,
        payment_sequential INT,
        payment_type TEXT,
        payment_installments INT,
        payment_value REAL,
        PRIMARY KEY (order_id, payment_sequential),
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );

    CREATE TABLE order_reviews (
        review_id TEXT PRIMARY KEY,
        order_id TEXT,
        review_score INT,
        review_comment_title TEXT,
        review_comment_message TEXT,
        review_creation_date TIMESTAMP,
        review_answer_timestamp TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );

    """))

print("Tables created")

# =========================
# LOAD CSV FILES
# =========================

data_paths = {
    'customers': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_customers_dataset.csv',
    'orders': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_orders_dataset.csv',
    'order_items': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_order_items_dataset.csv',
    'products': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_products_dataset.csv',
    'payments': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_order_payments_dataset.csv',
    'order_reviews': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_order_reviews_dataset.csv',
    'sellers': 'D:/Estudo/Portfolio/E-Commerce Analytics/data/olist_sellers_dataset.csv'
}

dfs = {name: pd.read_csv(path) for name, path in data_paths.items()}

print("CSVs loaded")

# =========================
# CLEAN PRIMARY KEYS
# =========================

primary_keys = {
    'customers': ['customer_id'],
    'sellers': ['seller_id'],
    'orders': ['order_id'],
    'products': ['product_id'],
    'order_reviews': ['review_id'],
    'order_items': ['order_id', 'order_item_id'],
    'payments': ['order_id', 'payment_sequential']
}

for table_name, df in dfs.items():
    if table_name in primary_keys:
        pk_cols = primary_keys[table_name]

        before = df.shape[0]

        df = df.drop_duplicates(subset=pk_cols)
        df = df.dropna(subset=pk_cols)

        after = df.shape[0]

        print(f"{table_name}: {before - after} duplicates or invalid rows removed")

        dfs[table_name] = df

# =========================
# INSERT DATA INTO DATABASE
# =========================

dfs['customers'].to_sql('customers', engine, if_exists='append', index=False)
dfs['sellers'].to_sql('sellers', engine, if_exists='append', index=False)
dfs['orders'].to_sql('orders', engine, if_exists='append', index=False)
dfs['products'].to_sql('products', engine, if_exists='append', index=False)
dfs['order_items'].to_sql('order_items', engine, if_exists='append', index=False)
dfs['payments'].to_sql('payments', engine, if_exists='append', index=False)
dfs['order_reviews'].to_sql('order_reviews', engine, if_exists='append', index=False)

print('CSV data inserted into Database')