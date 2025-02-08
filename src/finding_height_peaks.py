import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Compute statistics
mean_az = df["az"].mean()
median_az = df["az"].median()
std_az = df["az"].std()
min_az = df["az"].min()
max_az = df["az"].max()
q75, q25 = df["az"].quantile([0.75, 0.25])
iqr = q75 - q25

# Compute height dynamically
height = np.maximum(0, q75 + 0.5 * iqr)  # Use percentile-based approach

# Find peaks
peaks, _ = find_peaks(df["az"], height=height)

# Display results
print("peaks:", len(peaks))
print("mean:", mean_az)
print("median:", median_az)
print("std:", std_az)
print("min_az:", min_az)
print("max_az:", max_az)
print("q25:", q25)
print("q75:", q75)
print("IQR:", iqr)
print("height:", height)


# peaks: 1
# mean: -1.272025237619722
# median: -1.0638393876820151
# std: 0.4222818402255061
# min_az: -3.901362646549079
# max_az: 0.3389588151388096
# q25: -1.48282052962171
# q75: -1.0093757492713402
# IQR: 0.47344478035036985
# height: 0.0