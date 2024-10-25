import sys
import gc
import dask.dataframe as dd


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = dd.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')
        column = df['grade']

        for i in range(i):
            gc.collect()
            dd.concat([df, column], axis=1)
        
    except ValueError as e:
        print("error " + str(e))