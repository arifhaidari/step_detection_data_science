import os
import json
import pandas as pd
import joblib
import numpy as np
import logging
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# spikes start from in az
HEIGHT = -1.66

# Paths
# absolute path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "../data/data_raw")
MODEL_PATH = os.path.join(PROJECT_ROOT, "../models", "random_forest_model.pkl")
JSON_FILE_PATH = os.path.join(PROJECT_ROOT, "../data/data_output", "calculated_steps.json")

# relative path (if you want to run from inside the src folder)
# RAW_DATA_PATH = "../data/data_raw/"
# MODEL_PATH = "../models/random_forest_model.pkl"
# JSON_FILE_PATH = "../data/data_output/calculated_steps.json"

# Low-Pass Butterworth Filter
fs = 100.0  # Sampling frequency (Hz)
cutoff = 2.5  # Cutoff frequency (Hz)
order = 4  # Filter order

def butter_lowpass_filter(data, cutoff, fs, order=4):
    # The Nyquist frequency is the maximum frequency we can capture based on the sampling rate.
    nyquist = 0.5 * fs  
    # Normalizing the cutoff frequency ensures it's within the valid range [0,1] for the filter function.
    normal_cutoff = cutoff / nyquist 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)



def load_json_data(folder_path):
    data_list = []
    files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        df['id'] = file.split('.')[0]  
        df["time"] = pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S.%f", errors='coerce')
        # Handle cases where microseconds are missing
        df["time"].fillna(pd.to_datetime(df["time"], format="%Y-%m-%d %H:%M:%S", errors='coerce'), inplace=True)
        df['side'] = df['metadata'].apply(lambda x: x['side'])  # Extract side info
        df.drop(columns=['metadata'], inplace=True)

        data_list.append(df)

    return pd.concat(data_list, ignore_index=True)


def preprocess_data(df):
    # handle missing values
    df["time"] = df["time"].fillna(method="ffill")
    
    # setting the index
    df.set_index('time', inplace=True)
    df = df.sort_index()
    
    # extract the time difference between measurements
    df['time_diff'] = df.index.to_series().diff().dt.total_seconds()
    
    # Apply Low-Pass Butterworth Filter to sensor data columns
    # from .utils import butter_lowpass_filter
    sensor_columns = ["ax", "ay", "az", "gx", "gy", "gz"]
    
    for col in sensor_columns:
        df[col] = butter_lowpass_filter(df[col], cutoff, fs, order)
    return df


def extract_features(df):
    """
    Extracts features from raw sensor data at the session level.
    
    Parameters:
        df (pd.DataFrame): The sensor data containing columns ['id', 'time', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'side']
        time could come also as index for the dataframe as well
    
    Returns:
        pd.DataFrame: Processed session-level features with step counts.
    """
    # Ensure 'time' is a datetime type
    if df.get("time") is not None:
        if not pd.api.types.is_datetime64_any_dtype(df['time']):
            df["time"] = pd.to_datetime(df["time"])
        df.set_index('time', inplace=True)
        df = df.sort_index()
        
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    
    # Aggregate sensor statistics per session
    session_features = df.groupby("id").agg({
        "ax": ["mean", "std", "min", "max"],
        "ay": ["mean", "std", "min", "max"],
        "az": ["mean", "std", "min", "max"],
        "gx": ["mean", "std", "min", "max"],
        "gy": ["mean", "std", "min", "max"],
        "gz": ["mean", "std", "min", "max"]
        # "time_diff": ["sum", "count"]  # Sum gives session duration
    }).reset_index()

    # Flatten MultiIndex columns
    session_features.columns = ["_".join(col).strip() for col in session_features.columns.values]
    session_features = session_features.rename(columns={"id_": "id"})

    # Function to count steps using peaks in 'az'
    def count_peaks(series):
        peaks, _ = find_peaks(series, height=HEIGHT)  
        return len(peaks)
    
    # Count steps based on side (L or R)
    step_counts = df.groupby(["id", "side"])["az"].apply(count_peaks).unstack(fill_value=0)
    
    # Check if 'side' values contain 'L' (left) and 'R' (right), then assign them explicitly
    if 'L' in step_counts.columns:
        step_counts['left_steps'] = step_counts['L']
    else:
        step_counts['left_steps'] = 0

    if 'R' in step_counts.columns:
        step_counts['right_steps'] = step_counts['R']
    else:
        step_counts['right_steps'] = 0

    # Remove the temporary 'L' and 'R' columns to avoid keeping them in the final output
    step_counts = step_counts.drop(columns=['L', 'R'], errors='ignore')

    # merge all data
    final_df = session_features.merge(step_counts, on="id")
    
    # Extract time-based features
    final_df['session_duration'] = (df.index.max() - df.index.min()).total_seconds()
    final_df['num_measurements'] = len(df)
    final_df['start_time'] = df.index.min()
    final_df['end_time'] = df.index.max()

    return final_df


# Generate Predictions for a New Session
def predict_steps(new_session_data, loaded_model):
    new_session_features = extract_features(new_session_data)  

    # Extract only model input features
    X_new = new_session_features.drop(columns=["id", "start_time", "end_time", "left_steps", "right_steps"])

    # Predict step counts
    predicted_steps = loaded_model.predict(X_new)

    # Convert predictions to a structured output
    new_session_features["left_steps_pred"] = predicted_steps[:, 0].round().astype(int)
    new_session_features["right_steps_pred"] = predicted_steps[:, 1].round().astype(int)

    # Convert timestamps to string format
    new_session_features["start_time"] = new_session_features["start_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    new_session_features["end_time"] = new_session_features["end_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    # Final structured output
    output = new_session_features[["id", "start_time", "end_time", "left_steps_pred", "right_steps_pred"]]
    output.rename(columns={"left_steps_pred": "left_steps", "right_steps_pred": "right_steps"}, inplace=True)

    return output.to_dict(orient="records")


def generate_calculated_json(df, model):
    # Get unique IDs in the dataframe
    unique_ids = df["id"].unique()

    # Initialize an empty list to store results
    all_predictions = []

    # Loop through each unique ID, filter the dataframe, and make predictions
    for unique_id in unique_ids:
        session_data = df[df["id"] == unique_id]  # Get the part of df matching the unique ID
        predictions = predict_steps(session_data, model)  # Predict steps
        all_predictions.extend(predictions)  # Append results to the list

    # Save the results to a JSON file
    with open(JSON_FILE_PATH, "w") as f:
        json.dump(all_predictions, f, indent=4)

    print("Predictions saved to calculated_steps.json")


if __name__ == "__main__":
    print('loading the data ...')
    df = load_json_data(RAW_DATA_PATH)
    print('data is loaded')
    if df.empty:
        logging.error("No data found! Exiting.")
        exit()
    df = preprocess_data(df)
    print('data is processed')
    model = joblib.load(MODEL_PATH)
    
    # for multiple measurement
    generate_calculated_json(df, model)
    print('step is calculated')
    
    print("SUCCESS")
    
    # for a single measurement
    # predict_steps(single_session, model)
    
    