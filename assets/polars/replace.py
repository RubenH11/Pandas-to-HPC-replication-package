import sys
import gc
import polars as pl

if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = pl.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')
        
        valueToReplaceWithApple = 'OWN'
        for i in range(i):
            gc.collect()
            df.with_columns([pl.col(c).replace(valueToReplaceWithApple, 'apple') for c in df.select(pl.col(pl.String)).columns])
        
    except ValueError as e:
        print("error " + str(e))