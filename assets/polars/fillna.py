import sys
import gc
import polars as pl


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = pl.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')
        for i in range(i):
            gc.collect()
            df.fill_nan('apple')
        
    except ValueError as e:
        print("error " + str(e))