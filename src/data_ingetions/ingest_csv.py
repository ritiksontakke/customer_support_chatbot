import pandas as pd
from src.config.database import engine

df = pd.read_csv(
    "src/raw_data/customer_support_tickets_200k.csv"
)

print(df.shape)
print(df.head())

df.to_sql(
    "customer_support_tickets",
    engine,
    if_exists="append",
    index=False,
    chunksize=500,
    method="multi"
)

print("Data inserted successfully!")