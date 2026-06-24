from src.config.database import engine
import pandas as pd

df = pd.read_csv(
    "src/raw_data/customer_support_tickets_200k.csv"
)

# Date columns convert kar lo
df["ticket_created_date"] = pd.to_datetime(df["ticket_created_date"])
df["ticket_resolved_date"] = pd.to_datetime(df["ticket_resolved_date"])

df.to_sql(
    "customer_support_tickets",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=500,
    method="multi"
)

print("Data inserted successfully!")
