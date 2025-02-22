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


# using mean of acc_magnitude
mean_acc_magnitude = df["acc_magnitude"].mean()
std_acc_magnitude = df["acc_magnitude"].std()
mean_height = mean_acc_magnitude + 0.25 * std_acc_magnitude  

peaks, _ = find_peaks(df["acc_magnitude"], height=mean_height)

print("peaks", len(peaks))
print("mean_az",mean_acc_magnitude)
print("std_az",std_acc_magnitude)
print("height", height)

# peaks 352344
# mean_az 1.4666781837688312
# std_az 0.9405900599158591
# height 1.939164898253062