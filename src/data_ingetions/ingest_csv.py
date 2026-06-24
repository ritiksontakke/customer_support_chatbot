from src.config.database import engine
import pandas as pd

df = pd.read_csv(
    "src/raw_data/updated_users_roles_passwords.csv"
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