import sys
import gc
import pandas as pd


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = pd.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')
        
        column_name = 'loan_amnt'
        for i in range(i):
            gc.collect()
            df.sort_values(by=column_name)
        
    except ValueError as e:
        print("error " + str(e))