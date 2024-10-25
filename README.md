# Energy efficiency of Pandas versus HPC Libraries
Welcome to the replication package of the 'Energy efficiency of Pandas versus HPC Libraries' experiment. 
This page will guide you though the process of replicating the experiment described in its associated paper.

## Table of contents
- File structure
- Execution
  - Preparation
  - Running the experiment
- Analysis

## File structure
You will find two important folders that are specific to this experiment: `assets` and `experiment`. 
- `assets` holds all of the assets used to run this experiment. This includes a `data` folder, which will hold the datasets to operate on, and the python code to turn these CSV files into parquet files. (If you are interested in why we use parquets, please read the Threats to Validity section of the paper.) Additionally, it holds the code to the combination of all 4 libraries and 9 data frame operations. Each DFO finds itself within a folder named after the library under test. These files all accept the keyword 'small' or 'large' as an argument, indicating which dataset to operate one, as well as a number, indicating how many times the DFO should be executed within a single run.
- `experiment` holds the RunnerConfig.py file, which creates and populates the run table, handles measurements, and invokes the DFO files. After an execution of the experiment, it will also hold the run table and the logged measurements of runs in `runs/pandas_versus_hpc`.

You will also find a folder called `results`, which holds the raw measurement data that has been measured and analyzed for the paper.

## Execution
### Preparation
To get started, please clone this repository into your own device using the following command:
```
git clone https://github.com/RubenH11/Pandas-to-HPC-replication-package.git
```

Before you can execute the experiment, a few preparatory steps have to be taken.
Firstly, you shall need the datasets used in this experiment. `small.csv` has already been provided in this repository, but `large.csv` is too large to provide directly, which is why we ask you to download it though the following link: https://www.kaggle.com/datasets/debashis74017/stock-market-data-nifty-100-stocks-5-min-data 


Once this dataset has been installed, please rename it to `large.csv` and move it to `assets/data/`

Now execute the following command in your terminalfrom the root folder of the cloned project to turn your `large.csv` file into a `.parquet` file (this might take a while).
```
    python assets/data/createLargeParquet.py
```
With the datasets ready, we can proceed to installing the required packages and EnergiBridge by executing the following commands from the root folder (this might also take a while).

```
git clone https://github.com/tdurieux/EnergiBridge.git 
cd EnergiBridge
cargo build -r;
cd ..                          
pip install -r requirements.txt
```

### Running the experiment
To run the experiment, run the following command from the root folder.
```
python experiment-runner/ experiment/RunnerConfig.py
```
Note that this will will run the experiment at the following configuration:
- Iterations per run: 35 (a run should take at most 60s)
- Repetitions of runs: 20
- Cool-down time between runs: 20s
- Measurements occur every: 0.3s

## Analysis

## File Structure

The data analysis is divided into **four R Markdown files** located in the repository:

1. **H1_Pandas_vs_Polars_Small.Rmd** - Analysis of energy usage for small datasets.
2. **H1_Pandas_vs_Polars_Big.Rmd** - Analysis of energy usage for large datasets.
3. **H2_Correlation_Analysis.Rmd** - Correlation analysis between energy usage and other metrics.
4. **H2_Correlation_Analysis_Visuals.Rmd** - Visualization of the correlation analysis results.

### Required Data Files

The data needed for running the scripts are located in the **Data** folder:

- **Run_Table_DAT.csv** - Contains the run data for Data Analysis Tasks.
- **Run_Table_TPCH.csv** - Contains the run data for the TPCH Benchmarking.

Full runs from the experiment can be found in the following compressed files, also located in the **Data** folder:

- **TPCH-FULLRUN.zip** - Full runs for TPCH Benchmarking.
- **DAT-FULLRUN.zip** - Full runs for Data Analysis Tasks.

## Data Analysis Steps

### Measures of Central Tendency and Variability

- The analysis computes the **mean** and **median** for energy usage in the TPCH dataset, comparing Pandas and Polars across different dataframe sizes (Small and Big).
- It also calculates **standard deviation** and **variance** for further insights into the data distribution.

### Normality Checks

#### Visualize Data for Normality Checking
- Density and violin plots are generated to visualize the distribution of energy usage for both small and big datasets, comparing the two libraries.

#### QQ Plots
- Quantile-Quantile (QQ) plots are created to assess the normality of the data distribution for small and big datasets for both Pandas and Polars.

### Skewness and Transformations

- The analysis checks for data skewness (positive or negative) and applies transformations (square root or power) to enhance normality.
- The normality of the data is re-evaluated after transformations.

### Normality Testing on Original Data

- The **Shapiro-Wilk test** is conducted to assess the normality of the original data for both small and big datasets in Pandas and Polars, as well as for correlation analysis.

### Hypothesis Testing

- A **non-parametric Wilcoxon rank-sum test** is performed to compare energy usage between Pandas and Polars for both small and big datasets due to the non-normal distribution of the data.
- Scatterplots are created to visually check correlations between variables.

### Effect Size Estimation

- For the comparison between Pandas and Polars, **Cliff's Delta** is calculated for the big and small datasets separately, providing a measurement of effect size to quantify the differences in energy usage. Confidence intervals are also provided for interpretation.

## Running the Analysis

The R Markdown files can be executed in RStudio, either in separate chunks or all together. Make sure the required data files are placed in the appropriate **Data** folder for the scripts to run correctly.

## Conclusion

This analysis aims to provide a comprehensive understanding of the energy efficiency of high-performance Python libraries, contributing to the ongoing research in sustainable software engineering practices.

