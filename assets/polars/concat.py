import sys
import gc
import polars as pl


if __name__ == "__main__":

    csv_size = sys.argv[1]
    i = int(sys.argv[2])

    try:
        df = pl.read_parquet('assets/data/df_'+str(csv_size)+'_parquet.parquet')

        pdf_col_grade_as_renamed = df['grade'].alias('renamed').to_frame()
        column = pdf_col_grade_as_renamed

        for i in range(i):
            gc.collect()
            pl.concat([df, column], how='horizontal')
        
    except ValueError as e:
        print("error " + str(e))