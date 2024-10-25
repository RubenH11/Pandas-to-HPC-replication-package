import pandas as pd

df = pd.read_csv('assets/data/small.csv', low_memory=False)
df.to_parquet('assets/data/df_small_parquet.parquet')



