import joblib
from .data_processing import extract_features

def load_model(model_path):
     return joblib.load(model_path)

def predict_steps(new_session_data, model, height):
     new_session_features = extract_features(new_session_data)  
     X_new = new_session_features.drop(columns=["id", "start_time", "end_time", "left_steps", "right_steps"])

     predicted_steps = model.predict(X_new)
     
     new_session_features["left_steps_pred"] = predicted_steps[:, 0].round().astype(int)
     new_session_features["right_steps_pred"] = predicted_steps[:, 1].round().astype(int)

     new_session_features["start_time"] = new_session_features["start_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")
     new_session_features["end_time"] = new_session_features["end_time"].dt.strftime("%Y-%m-%dT%H:%M:%S")

     output = new_session_features[["id", "start_time", "end_time", "left_steps_pred", "right_steps_pred"]]
     output.rename(columns={"left_steps_pred": "left_steps", "right_steps_pred": "right_steps"}, inplace=True)

     return output.to_dict(orient="records")
