import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate 500 rows of sample data
num_rows = 500
start_time = datetime(2024, 6, 14, 8, 14, 33, 753000)

data = []
for i in range(num_rows):
    timestamp = start_time + timedelta(milliseconds=i * 100)  # Simulating 100ms intervals
    side = np.random.choice(["L", "R"])  # Randomly assign "L" or "R"
    
    # Generate random sensor values (simulating realistic ranges)
    gx, gy, gz = np.random.uniform(-2, 2, 3)  # Gyroscope values
    ax, ay, az = np.random.uniform(-1.5, 1.5, 3)  # Accelerometer values
    
    data.append([timestamp, side, gx, gy, gz, ax, ay, az])

# Create a DataFrame
df = pd.DataFrame(data, columns=["time", "side", "gx", "gy", "gz", "ax", "ay", "az"])

# Save to CSV
csv_file_path = "../data/sample_sensor_data.csv"
df.to_csv(csv_file_path, index=False)

csv_file_path