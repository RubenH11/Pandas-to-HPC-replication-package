import sys
import gc
import pandas as pd


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = pd.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')

        mdf_col_grade = df['grade']
        column = mdf_col_grade

        for i in range(i):
            gc.collect()
            pd.concat([df, column], axis=1) # 1 = columns
        
    except ValueError as e:
        print("error " + str(e))