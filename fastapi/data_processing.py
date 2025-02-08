def extract_features(df):
     # Feature extraction as before
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

     step_counts = df.groupby(["id", "side"])["az"].apply(count_peaks, height=HEIGHT).unstack(fill_value=0)
     
     if 'L' in step_counts.columns:
          step_counts['left_steps'] = step_counts['L']
     else:
          step_counts['left_steps'] = 0

     if 'R' in step_counts.columns:
          step_counts['right_steps'] = step_counts['R']
     else:
          step_counts['right_steps'] = 0

     step_counts = step_counts.drop(columns=['L', 'R'], errors='ignore')
     final_df = session_features.merge(step_counts, on="id")
     
     final_df['session_duration'] = (df.index.max() - df.index.min()).total_seconds()
     final_df['num_measurements'] = len(df)
     final_df['start_time'] = df.index.min()
     final_df['end_time'] = df.index.max()

     # Return predictions in the format for DB insertion
     predictions = final_df[["id", "start_time", "end_time", "left_steps", "right_steps"]].to_dict(orient="records")
     return predictions
