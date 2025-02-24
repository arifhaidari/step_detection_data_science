# Step Counting Model (Prediction) Correction

## Overview

Here I am gonna explain the corrections made to the step-counting model to improve its accuracy and not break the laws of physics again :)))). The primary changes involved modifying the filter, considering the time factor (0.5 second per step), using magnitude of linear acceleration and tuning parameters to achieve realistic predictions.

## Key Corrections

### 1. Adjusted Filtering and Parameter Tuning

One of the main improvements was modifying the filter used to detect steps and fine-tuning the parameters to align with realistic step durations.

A rough estimation of the time required to take a step:

- **0.5 seconds (half a second)** per step

### 2. Updated Code Implementation

The following Python code snippet demonstrates the updated approach:

```python
from scipy.signal import find_peaks

# calculate the magnitude of accelerometer
df['acc_magnitude'] = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)

# Compute mean height threshold
mean_height = df["acc_magnitude"].mean() + 0.5 * df["acc_magnitude"].std()

# Sampling rate in Hz (samples per second)
fs = 1 / df['time_diff'].median()

# Minimum distance between peaks (0.5 seconds per step) - a rough estimate
min_distance = int(0.5 * fs)

def count_peaks(series):
    peaks, _ = find_peaks(series, height=mean_height, distance=min_distance)
    return len(peaks)
```

### 3. Explanation of Variations in Readings

In some cases, there were fewer sensor readings within a given time period. This occurred due to:

- Variability in sensor readings
- Rest periods where the person was standing still or not moving linearly

### 4. Impact of `acc_magnitude`

- The **acc_magnitude** is directly proportional to step count (both left and right steps) and that is why it is chosen over only vertical acceleration.
- Other attributes contribute to step detection but not as significantly as **acc_magnitude**, which primarily defines the steps.

## Statistical Analysis

### Some Prediction (from actual dataset):

For more visit /data/data_output

```
[
    {
        "id": "MRBF3DNuWq0zhSXajwPy",
        "start_time": "2024-06-14T07:19:32.380000",
        "end_time": "2024-06-14T07:19:44.425000",
        "left_steps": 6,
        "right_steps": 6,
        "session_duration": 12.045,
        "num_measurements": 9530
    },
    {
        "id": "CiebYhzPBsVTxlm2R5YC",
        "start_time": "2024-06-14T07:22:59.098000",
        "end_time": "2024-06-14T07:23:12.237000",
        "left_steps": 6,
        "right_steps": 7,
        "session_duration": 13.139,
        "num_measurements": 10438
    },
]
```

## Additional Improvements

Another critical improvement was applying **low-pass filtering** to smooth out sensor data and reduce noise, making step detection more robust.

## Validation Against External Data

According to research, the average number of steps per minute is approximately **100 steps per minute** (50 left and 50 right steps) [(Source)](https://bjsm.bmj.com/content/52/12/776). The updated model aligns well with this benchmark and remains within the physical constraints of human walking.

## References

- [Step Counting Research & Methodology](https://dganesan.github.io/mhealth-course/chapter2-steps/ch2-stepcounter.html)
- [Walking Cadence and Human Step Rates](https://bjsm.bmj.com/content/52/12/776)
