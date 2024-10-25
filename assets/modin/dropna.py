import sys
import gc
import modin.pandas as pd
import ray


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        # ray.init()
        df = pd.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')
        for i in range(i):
            gc.collect()
            df.dropna()
        # ray.shutdown()
        
    except ValueError as e:
        print("error " + str(e))