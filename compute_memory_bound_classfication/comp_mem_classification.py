import pandas as pd
import numpy as np
import time
from memory_profiler import memory_usage

# Function to measure FLOPs and memory access for specific operations
def measure_operation(func, *args, **kwargs):
    # Measure memory usage before the operation
    mem_before = memory_usage()[0]
    
    # Measure execution time
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()

    # Measure memory usage after the operation
    mem_after = memory_usage()[0]

    # Calculate time taken in seconds
    time_taken = end_time - start_time
    
    return time_taken, mem_before, mem_after

# Sample DataFrame for testing
data_size = 1_000_000  # Number of rows
df = pd.DataFrame({
    'A': np.random.rand(data_size),
    'B': np.random.rand(data_size)
})

# Introduce some NaN values (10% of the 'B' column)
nan_indices = np.random.choice(df.index, size=int(data_size * 0.1), replace=False)  # 10% NaN
df.loc[nan_indices, 'B'] = np.nan  # Assign NaN to 10% of 'B' column

# Display the DataFrame and count NaNs
print("Count of NaN values in each column:")
print(df.isna().sum())  # Count NaNs in each column

# Operations to measure with rough FLOPs estimates
operations = {
    "replace": lambda: df.replace({1: 0}),   # Replace 1 with 999   # Roughly data_size
    "isna": lambda: df.isna(),                     # Roughly data_size
    "concat": lambda: pd.concat([df, df]),        # Roughly 2 * data_size
    "mean": lambda: df['A'].mean(),               # Roughly data_size
    "sort": lambda: df.sort_values(by='A'),       # Roughly data_size * log(data_size)
    "groupby": lambda: df.groupby('B'),    # Roughly data_size for each group
    "fillna": lambda: df.fillna(np.nan),                 # Roughly data_size
    "dropna": lambda: df.dropna(),                # Varies based on NaNs
    "drop": lambda: df.drop(columns=['A']),       # Roughly data_size
}

# Step 4: Measure FLOPs and memory access for each operation
results = {}
for name, operation in operations.items():
    time_taken, mem_before, mem_after = measure_operation(operation)
    
    # Calculate FLOPs and memory access
    if name == "concat":
        flops = 2 * data_size  # Two copies being concatenated
    elif name == "drop":
        flops = data_size  # One pass through the data
    elif name == "dropna":
        flops = data_size  # Assume each row is checked
    elif name == "mean":
        flops = data_size  # Sum and divide by count
    elif name == "sort":
        flops = data_size * np.log2(data_size)  # Logarithmic time complexity
    elif name == "groupby":
        flops = data_size  # One pass through the data
    elif name == "replace":
        flops = data_size  # One pass through the data
    elif name == "isna":
        flops = data_size  # One check per row
    elif name == "fillna":
        flops = data_size  # One pass through the data
    else:
        flops = 0  # Default if operation is unknown

    # Memory access in bytes
    memory_access = (mem_after - mem_before) * 1e6  # Convert to bytes

    # Store results
    results[name] = {"flops": flops, "memory_access": memory_access}

# Define a threshold for operational intensity
OI_THRESHOLD = 1  # Example: Threshold value to separate compute-bound and memory-bound operations

# Function to classify each operation
def classify_operation(operation):
    flops = operation["flops"]
    memory_access = operation["memory_access"]
    
    # Calculate Operational Intensity (OI)
    OI = flops / memory_access if memory_access > 0 else float('inf')  # Avoid division by zero
    
    # Classify the operation based on the threshold
    classification = "Compute-bound" if OI >= OI_THRESHOLD else "Memory-bound"
    
    return OI, classification

# Step 5: Classify each operation and display the results
print("\nClassification of Operations:")

# Initialize dictionaries to group results
grouped_results = {
    "Compute-bound": [],
    "Memory-bound": []
}

for name, metrics in results.items():
    OI, classification = classify_operation(metrics)
    grouped_results[classification].append({
        "name": name,
        "flops": metrics['flops'],
        "memory_access": metrics['memory_access'] / 1e6,  # Convert to MB
        "OI": OI
    })

# Display grouped results
for bound_type, ops in grouped_results.items():
    print(f"\n{bound_type} Operations:")
    for op in ops:
        print(f"{op['name']}: FLOPs = {op['flops']}, Memory Access = {op['memory_access']:.2f} MB, OI = {op['OI']:.2f}")
