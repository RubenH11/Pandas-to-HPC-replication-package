import pandas as pd

df = pd.read_csv('assets/data/large.csv', low_memory=False)
df.to_parquet('assets/data/df_large_parquet.parquet')



