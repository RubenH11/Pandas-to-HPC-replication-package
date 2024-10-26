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
Note that this will run the experiment at the following configuration:
- Iterations per run: 35 (a run should take at most 60s)
- Repetitions of runs: 20
- Cool-down time between runs: 20s
- Measurements occur every: 0.3s

# Data Analysis

## Folder Structure

The analysis part is organized into the following folders and files:

### **Data Analysis Folder (`/Data analysis/`)**
This folder contains all R Markdown (`.Rmd`) files used for data analysis, statistical testing, and visualizations. Each file addresses specific aspects of the analysis:

1. **`EDA_Statistical_analysis.Rmd`**: Conducts exploratory data analysis (EDA) with a focus on statistical summaries and measures of central tendency (mean, median, variance, standard deviation) for energy efficiency and performance metrics across libraries and dataset sizes.

2. **`EDA_Visual_analysis.Rmd`**: Contains visual EDA methods, generating plots (density, box plots) for an overview of data distribution, energy efficiency, and performance across libraries.

3. **`Normality_testing.Rmd`**: Checks for data normality using the Shapiro-Wilk test, QQ-plots, and skewness assessments. The BestNormalize transformation is applied if skewness is identified, with normality re-evaluated post-transformation.

4. **`RQ1_H.Rmd`**: Compares energy efficiency between Pandas and other HPC libraries (Polars, Dask, Modin), analyzing both small and large datasets.

5. **`RQ2_H.Rmd`**: Compares energy efficiency across libraries, focusing on memory-bound versus compute-bound DataFrame operations (DFOs) for Pandas and HPC libraries.

6. **`RQ3_H.Rmd`**: Explores correlations between energy efficiency and execution metrics (execution time, CPU usage, memory usage) across libraries.

7. **`further_research.Rmd`**: Provides additional analysis focused on comparing Polars and Dask, analyzing energy efficiency both overall and across specific DFOs (memory-bound and compute-bound).

### **Figures Folder (`/Figures/`)**
Contains generated figures and visualizations from the analysis scripts.

### **Data Files**
- **`run_table.csv`**: Main dataset containing experiment results used across all `.Rmd` files for analysis and statistical testing.

#### Alternatively, you can view the results of our analysis in Jupyter notebooks [here](https://drive.google.com/drive/folders/1HalwpTdJYJ_vVkxWj5tTQ5wIfLsPoFgy?usp=sharing). Do not forget to change runtime to "R" if you intend to run the notebooks.

## Data Analysis Summary

### Measures of Central Tendency and Variability
- EDA scripts calculate mean, median, variance, and standard deviation for energy efficiency and execution metrics across libraries (Pandas, Polars, Dask, Modin) and data sizes (small and large).

### Normality Checks
- **Shapiro-Wilk Test**: Used to assess the normality of the data.
- **Visualizations**: Density and QQ-plots illustrate distribution patterns.
- **Transformations**: BestNormalize function applies transformations to reduce skewness, improving data normality.


### Hypothesis Testing

- RQ1 and RQ2: A **non-parametric Wilcoxon rank-sum test** is performed to compare energy usage between the pairs of libraries in question (eg. Pandas-Polars, Pandas-Modin, etc.) for both small and large datasets due to the non-normal distribution of the data.
- RQ3:
- -- Scatterplots are created to visually check correlations between energy efficiency of the library in question, and each of three metrics - execution time, cpu usage and memory usage.
- -- Spearman's rank correlation is used for calculating correlation coefficient rho between the two metrics in question

### Effect Size Estimation

- For the comparison within the pair of libraries in question (eg. Pandas - Polars), **Cliff's Delta** is calculated for the big and small datasets separately, providing a measurement of effect size to quantify the differences in energy usage. Confidence intervals are also provided for interpretation.
- Spearman's rank correlation method also calculates p-value which is used for estimating effect size for correlation between the metrics

## Running the Analysis

The R Markdown files can be executed in RStudio, either in separate chunks or all together. Make sure the required data files are placed in the appropriate **Data** folder for the scripts to run correctly. Make sure that your working directory is correctly set to the right directory where both the rmd and data files are located.

