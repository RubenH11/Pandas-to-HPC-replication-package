import sys
import gc
import dask.dataframe as dd


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = dd.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')

        mdf_col_loan_amount = df['loan_amnt'].compute()
        for i in range(i):
            gc.collect()
            mdf_col_loan_amount.mean()

    except ValueError as e:
        print("error " + str(e))