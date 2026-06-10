import pandas as pd
from sqlalchemy import create_engine

# 1. Paste your External Database URL from Render here
DATABASE_URL = "postgresql://triage_db_i5sf_user:Um5MLaKyiwkE6Vd4wNWFQOTv1t6nOUhV@dpg-d8kpgjegvqtc73fm34b0-a.oregon-postgres.render.com/triage_db_i5sf"

# 2. Connect to the cloud database
engine = create_engine(DATABASE_URL)

# 3. Read your local CSV
print("Reading local CSV...")
df = pd.read_csv("donors.csv")

# 4. Upload the whole table to PostgreSQL
print("Pushing data to cloud database...")
df.to_sql('donors_table', engine, if_exists='replace', index=False)

print("Success! Your CSV data is now living in the cloud.")