import pandas as pd
from scipy.signal import find_peaks, butter, filtfilt

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Constants
HEIGHT = -1.66
fs = 100.0  # Sampling frequency (Hz)
cutoff = 2.5  # Cutoff frequency (Hz)
order = 4  # Filter order



class DataPreprocessor:
     @staticmethod
     def butter_lowpass_filter(data, cutoff, fs, order=4):
          nyquist = 0.5 * fs
          normal_cutoff = cutoff / nyquist
          b, a = butter(order, normal_cutoff, btype='low', analog=False)
          return filtfilt(b, a, data)
     
     def preprocess(self, df):
          # Convert 'time' column to datetime
          df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S.%f", errors="coerce")
          
          # Fill missing time values using forward fill
          df["time"] = df["time"].ffill()
          
          df.set_index('time', inplace=True)
          df = df.sort_index()
          df['time_diff'] = df.index.to_series().diff().dt.total_seconds()
          sensor_columns = ["ax", "ay", "az", "gx", "gy", "gz"]
          for col in sensor_columns:
               df[col] = self.butter_lowpass_filter(df[col], cutoff, fs, order)
          return df

class FeatureExtractor:
     @staticmethod
     def extract_features(df):
          if df.get("time") is not None:
               df["time"] = pd.to_datetime(df["time"])
               df.set_index('time', inplace=True)
               df = df.sort_index()
          df.index = pd.to_datetime(df.index)
          session_features = df.groupby("id").agg({
               "ax": ["mean", "std", "min", "max"],
               "ay": ["mean", "std", "min", "max"],
               "az": ["mean", "std", "min", "max"],
               "gx": ["mean", "std", "min", "max"],
               "gy": ["mean", "std", "min", "max"],
               "gz": ["mean", "std", "min", "max"]
          }).reset_index()
          session_features.columns = ["_".join(col).strip() for col in session_features.columns.values]
          session_features = session_features.rename(columns={"id_": "id"})
          def count_peaks(series):
               peaks, _ = find_peaks(series, height=HEIGHT)
               return len(peaks)
          step_counts = df.groupby(["id", "side"])["az"].apply(count_peaks).unstack(fill_value=0)
          step_counts['left_steps'] = step_counts.get('L', 0)
          step_counts['right_steps'] = step_counts.get('R', 0)
          final_df = session_features.merge(step_counts, on="id")
          final_df['session_duration'] = (df.index.max() - df.index.min()).total_seconds()
          final_df['num_measurements'] = len(df)
          final_df['start_time'] = df.index.min()
          final_df['end_time'] = df.index.max()
          return final_df