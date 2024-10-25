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

Now execute the following command in your terminal <u>from the root folder of the cloned project</u> to turn your `large.csv` file into a `.parquet` file.
```
    python assets/data/createLargeParquet.py
```
With the datasets ready, we can proceed to installing the required packages and EnergiBridge by executing the following commands <u>from the root folder</u>.

```
git clone https://github.com/tdurieux/EnergiBridge.git 
cd EnergiBridge
cargo build -r;
cd ..                          
pip install -r requirements.txt
```

### Running the experiment
To run the experiment, run the following command <u>from the root folder</u>.
```
python experiment-runner/ experiment/RunnerConfig.py
```
Note that this will will run the experiment at the following configuration:
- Iterations per run: 35 (a run should take at most 60s)
- Repetitions of runs: 20
- Cool-down time between runs: 20s
- Measurements occur every: 0.3s

## Analysis