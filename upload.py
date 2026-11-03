import os
import pandas as pd
import hana_ml.dataframe as dataframe
HANA_ADDRESS = os.environ.get('HANA_ADDRESS')
HANA_USERNAME= os.environ.get('HANA_USERNAME')
HANA_PASSWORD= os.environ.get('HANA_PASSWORD')

print(f"DEBUG ADDRESS: {HANA_ADDRESS}")
print(f"DEBUG USER: {HANA_USERNAME}")
print(f"DEBUG PASSWORD LENGTH: {len(HANA_PASSWORD) if HANA_PASSWORD else 'ESTA VACIO'}")

conn = dataframe.ConnectionContext(address=HANA_ADDRESS,
                                   port=443, 
                                   user=HANA_USERNAME, 
                                   password=HANA_PASSWORD 
                                   )

print(f"Connected successfully: {conn.connection.isconnected()}")

df = pd.read_csv("housing.csv")
df = df.reset_index()
df.columns = map(str.upper, df.columns)
df['INDEX'] = df['INDEX'].astype('str')

hana_df = dataframe.create_dataframe_from_pandas(
    connection_context=conn,
    pandas_df=df,
    table_name="HOUSING",
    primary_key="index",
    force=True,     # Set to True to drop/truncate existing tables
    replace=False   # Set to True to map NULLs to 0/empty strings
)

print("Upload complete!")
conn.close()