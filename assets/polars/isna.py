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
            df.select(pl.col(pl.Float64, pl.Float32, pl.Int64, pl.Int32, pl.Int16, pl.Int8).is_nan())
        
    except ValueError as e:
        print("error " + str(e))