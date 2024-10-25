from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ExtendedTyping.Typing import SupportsStr
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, Optional
from pathlib import Path
from os.path import dirname, realpath

import os
import gc
import subprocess
import shlex
import pandas as pd
import psutil

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    """The name of the experiment."""
    name:                       str             = "pandas_versus_hpc"

    """The path in which Experiment Runner will create a folder with the name `self.name`, in order to store the
    results from this experiment. (Path does not need to exist - it will be created if necessary.)
    Output path defaults to the config file's path, inside the folder 'runs'"""
    results_output_path:        Path            = ROOT_DIR / 'runs'

    """Experiment operation type. Unless you manually want to initiate each run, use `OperationType.AUTO`."""
    operation_type:             OperationType   = OperationType.AUTO

    """The time Experiment Runner will wait after a run completes.
    This can be essential to accommodate for cooldown periods on some systems."""
    time_between_runs_in_ms:    int             = 20000

    i = 35
    interval_ms=300
    process=""

    # Dynamic configurations can be one-time satisfied here before the program takes the config as-is
    # e.g. Setting some variable based on some criteria
    def __init__(self):
        """Executes immediately after program start, on config load"""
        output.console_log(os.getcwd())

        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN       , self.before_run       ),
            (RunnerEvents.START_RUN        , self.start_run        ),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT         , self.interact         ),
            (RunnerEvents.STOP_MEASUREMENT , self.stop_measurement ),
            (RunnerEvents.STOP_RUN         , self.stop_run         ),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT , self.after_experiment )
        ])
        self.run_table_model = None  # Initialized later

        output.console_log("Custom config loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create and return the run_table model here. A run_table is a List (rows) of tuples (columns),
        representing each run performed"""
        factor1 = FactorModel("Library", ['Modin', 'Dask', 'Pandas', 'Polars'])
        factor2 = FactorModel("DataFrame size", ['Large', 'Small'])
        subject = FactorModel("DFO", ['isna', 'replace', 'groupby', 'sort', 'mean', 'drop', 'dropna', 'fillna', 'concat'])

        self.run_table_model = RunTableModel(
            factors=[subject, factor1, factor2],
            repetitions = 20,
            data_columns=['execution_time', 'num_dfos_per_joule', 'cpu_utilisation', 'memory_usage']
        )
        return self.run_table_model

    def before_experiment(self) -> None:
        """Perform any activity required before starting the experiment here
        Invoked only once during the lifetime of the program."""
        pass

    def before_run(self) -> None:
        """Perform any activity required before starting a run.
        No context is available here as the run is not yet active (BEFORE RUN)"""
        pass

    def start_run(self, context: RunnerContext) -> None:
        """Perform any activity required for starting the run here.
        For example, starting the target system to measure.
        Activities after starting the run should also be performed here."""
        gc.collect()

    def start_measurement(self, context: RunnerContext) -> None:
        """Perform any activity required for starting measurements."""
        library = context.run_variation['Library']
        dfo = context.run_variation['DFO']
        df_size = context.run_variation['DataFrame size']
        output.console_log(library)
        output.console_log(dfo)
        output.console_log(df_size)

        profiler_cmd = f'EnergiBridge/target/release/energibridge \
            --interval {self.interval_ms} \
            --output {context.run_dir / "energibridge.csv"} \
            --summary \
            python assets/{library}/{dfo}.py {df_size} {self.i}'
        
        energibridge_log = open(f'{context.run_dir}/energibridge.log', 'w')

        self.process = psutil.Process()
        self.process.cpu_percent(interval=None)
        self.profiler = subprocess.Popen(shlex.split(profiler_cmd), stdout=energibridge_log)

    def interact(self, context: RunnerContext) -> None:
        """Perform any interaction with the running target system here, or block here until the target finishes."""
        pass

    def stop_measurement(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping measurements."""        
        self.cpu_usage = self.process.cpu_percent(interval=None)
        self.profiler.wait()

    def stop_run(self, context: RunnerContext) -> None:
        """Perform any activity here required for stopping the run.
        Activities after stopping the run should also be performed here."""

        gc.collect()

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, SupportsStr]]:
        """Parse and process any measurement data here.
        You can also store the raw measurement data under `context.run_dir`
        Returns a dictionary with keys `self.run_table_model.data_columns` and their values populated"""

        df = pd.read_csv(context.run_dir / "energibridge.csv")
        with open(context.run_dir / "energibridge.log", "r") as reader:
            contents = reader.read()

        execution_time = (contents.split('for ')[1]).split(' sec')[0]
        energy_joules = (contents.split('joules: ')[1]).split(' for ')[0]
        execution_time = float(execution_time)
        energy_joules = float(energy_joules)

        dfo_per_joules = self.i / energy_joules

        run_data = {
            'execution_time'        :   round(execution_time, 3), 
            'num_dfos_per_joule'    :   round(dfo_per_joules, 3),
            'cpu_utilisation'       :   self.cpu_usage,   
            'memory_usage'          :   round(df['USED_MEMORY'].mean(), 3),
        }

        return run_data

    def after_experiment(self) -> None:
        """Perform any activity required after stopping the experiment here
        Invoked only once during the lifetime of the program."""
        pass

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path:            Path             = None
