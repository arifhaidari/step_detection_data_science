import pandas as pd
from scipy.signal import find_peaks, butter, filtfilt
import numpy as np

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Constants (Low-Pass filter)
cutoff = 5  # Cutoff frequency (Hz)
order = 4  # Filter order


class DataPreprocessor:
     @staticmethod
     def low_pass_filter(data, cutoff, fs, order=4):
          nyquist = 0.5 * fs  # Nyquist Frequency
          normal_cutoff = cutoff / nyquist
          b, a = butter(order, normal_cutoff, btype='low', analog=False)
          return filtfilt(b, a, data)
     
     def preprocess(self, df):
          # Fill missing time values using forward fill
          df["time"] = df["time"].ffill()
          
          df.set_index('time', inplace=True)
          df = df.sort_index()
          df['time_diff'] = df.index.to_series().diff().dt.total_seconds()
          fs = 1 / df['time_diff'].median()  # Hz (sampling frequency)
          sensor_columns = ["gx", "gy", "gz"]
          for col in sensor_columns:
               df[col] = self.low_pass_filter(df[col], cutoff, fs, order)
               
          df['acc_magnitude'] = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)
          df['gyro_magnitude'] = np.sqrt(df['gx']**2 + df['gy']**2 + df['gz']**2)
          return df

class FeatureExtractor:
     @staticmethod
     def extract_features(df):
          # Reset index to bring 'time' back as a column
          df_reset = df.reset_index()

          # Group by 'id' and aggregate numerical features
          session_features = df_reset.groupby("id").agg({
          "ax": ["mean", "std", "min", "max"],
          "ay": ["mean", "std", "min", "max"],
          "az": ["mean", "std", "min", "max"],
          "gx": ["mean", "std", "min", "max"],
          "gy": ["mean", "std", "min", "max"],
          "gz": ["mean", "std", "min", "max"],
          "acc_magnitude": ["mean", "std", "min", "max"],
          "gyro_magnitude": ["mean", "std", "min", "max"],
          }).reset_index()

          # Flatten MultiIndex column names
          session_features.columns = ["_".join(col).strip() for col in session_features.columns.values]
          session_features = session_features.rename(columns={"id_": "id"})

          # Compute start_time and end_time
          time_stats = df_reset.groupby("id")["time"].agg(["min", "max"]).reset_index()
          time_stats.rename(columns={"min": "start_time", "max": "end_time"}, inplace=True)

          # Calculate session duration in seconds
          time_stats["session_duration"] = (time_stats["end_time"] - time_stats["start_time"]).dt.total_seconds()

          # Calculate num_measurements using size()
          num_measurements = df_reset.groupby("id").size().reset_index(name="num_measurements")

          # Merge all computed features
          session_features = session_features.merge(time_stats, on="id").merge(num_measurements, on="id")
          
          # Calculating the height (threshold to detect the steps from signals)
          mean_height = df["acc_magnitude"].mean() + 0.5 * df["acc_magnitude"].std()  
          
          # Sampling rate & one step duration (estimation)
          fs = 1 / df['time_diff'].median()  # Sampling rate in Hz (samples / seconds)
          min_distance = int(0.5 * fs)  # Minimum distance between peaks (0.5 seconds)
          # every step takes around 0.5 seconds
          
          # calculate the steps
          def count_peaks(series):
               peaks, _ = find_peaks(series, height=mean_height, distance=min_distance)  
               return len(peaks)

          # Count steps based on side (L or R)
          step_counts = df.groupby(["id", "side"])["acc_magnitude"].apply(count_peaks).unstack(fill_value=0)

          # Check if 'side' values contain 'L' (left) and 'R' (right), then assign them explicitly
          step_counts['left_steps'] = step_counts.get('L', 0)
          step_counts['right_steps'] = step_counts.get('R', 0)

          # Remove the temporary 'L' and 'R' columns to avoid keeping them in the final output
          step_counts = step_counts.drop(columns=['L', 'R'], errors='ignore')

          final_df = session_features.merge(step_counts, on="id")
          return final_df