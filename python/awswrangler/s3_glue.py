import awswrangler as wr
import pandas as pd

# Glue Catalog : https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/005%20-%20Glue%20Catalog.ipynb
# Partition Projection : https://github.com/awslabs/aws-data-wrangler/blob/main/tutorials/017%20-%20Partition%20Projection.ipynb
path = f"s3://test/data/"

df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["shoes", "tshirt", "ball"],
    "price": [50.3, 10.5, 20.0],
    "in_stock": [True, True, False]
})

#%% show databases

databases = wr.catalog.databases()
print(databases)

#%% create database
if "awswrangler_test" not in databases.values:
    wr.catalog.create_database("awswrangler_test")
    print(wr.catalog.databases())
else:
    print("Database awswrangler_test already exists")

#%% show tables
wr.catalog.tables(database="awswrangler_test")
wr.catalog.tables(name_contains="roduc")
wr.catalog.tables(name_prefix="pro")
wr.catalog.tables(name_suffix="ts")
wr.catalog.tables(search_text="This is my") # able to search on description as well.

#%% show table detail
wr.catalog.table(database="awswrangler_test", table="products")


#%% write to glue simple
wr.s3.to_parquet(
    df=df,
    path=path,
    dataset=True,
    mode="overwrite",
    database="aws_data_wrangler",
    table="my_table"
)

#%% write to glue with description
desc = "This is my product table."

param = {
    "source": "Product Web Service",
    "class": "e-commerce"
}

comments = {
    "id": "Unique product ID.",
    "name": "Product name",
    "price": "Product price (dollar)",
    "in_stock": "Is this product availaible in the stock?"
}

res = wr.s3.to_parquet(
    df=df,
    path=f"s3://test/products/",
    dataset=True,
    database="awswrangler_test",
    table="products",
    mode="overwrite",
    description=desc,
    parameters=param,
    columns_comments=comments
)
#%% store metadata of s3 path
res = wr.s3.store_parquet_metadata(
    path=path,
    database="awswrangler_test",
    table="crawler",
    dataset=True,
    mode="overwrite",
    dtype={"year": "int"}  # set type for certain columns if required
)


#%% read from glue
wr.athena.read_sql_query("SELECT * FROM my_table", database="aws_data_wrangler")

# add categories to speed up and save memory
wr.athena.read_sql_query("SELECT * FROM noaa", database="awswrangler_test", categories=["id", "dt", "element", "value", "m_flag", "q_flag", "s_flag", "obs_time"])

#%% batch(for restricted memory environment)
dfs = wr.athena.read_sql_query(
    "SELECT * FROM noaa",
    database="awswrangler_test",
    chunksize=True  # Chunksize calculated automatically for ctas_approach.
)
dfs = wr.athena.read_sql_query(
    "SELECT * FROM noaa",
    database="awswrangler_test",
    chunksize=100_000_000
)

for df in dfs:  # Batching
    print(len(df.index))

#%% delete table
wr.catalog.delete_table_if_exists(database="awswrangler_test", table="noaa")

#%% delete database
wr.catalog.delete_database('awswrangler_test')
