# Step Detection - Data Science

## 📌 Project Overview

This project was developed as part of a task assigned by **EVERSION Technologies GmbH** to evaluate my data science skills. The objective is to build a step detection model using sensor data and apply machine learning techniques to predict the total number of steps taken in a session (measurement).

## 🚀 How to Run the Project

To set up and run the project on your system, follow the step-by-step guide provided here:
🔗 [How to Run](https://github.com/arifhaidari/step_detection_data_science/blob/main/how_to_run.md)

## 📖 Problem Definition

Step detection plays a crucial role in various applications, including fitness tracking, rehabilitation, and gait analysis. The goal of this project is to predict the total number of steps from sensor data.

- **Problem Type:** Regression
- **Why Regression?** The goal is to predict the total step count, which is a continuous numerical value.
- **Alternative Approach:** If the objective were to classify each time frame as "step" or "no step" for real-time detection, it could be framed as a classification problem.

## 🔬 Approach

### 1️⃣ Data Preprocessing

- Handling missing values and detecting spikes (which is considered to be a step) using filtering techniques.
- Extracting features from raw sensor data.

### 2️⃣ Feature Engineering

- Analyzing sensor signals to derive meaningful features.
- Evaluating feature importance for step count prediction.

### 3️⃣ Modeling

- Implemented a **Random Forest model** for step count prediction.
- Evaluated different machine learning models to optimize performance.

### 4️⃣ Evaluation & Deployment

- Analyzed model performance.
- Packaged the model using **FastAPI** and **Containerized** deployment.
- Provided a **Flutter-based visualization app**.

## 📂 Project Structure

```
.
├── Dockerfile
├── README.md
├── api
│   ├── config.py
│   ├── database.py
│   ├── database_temp
│   │   ├── db_connection.py
│   │   └── tables.py
│   ├── endpoints
│   │   ├── steps_crud_db.py
│   │   ├── steps_prediction_db.py
│   │   └── steps_prediction_json.py
│   ├── main.py
│   └── schema
│       └── prediction_schema.py
├── app
│   └── download_app.txt
├── data
│   ├── data_extracted
│   │   ├── feature_engineered_data.csv
│   │   ├── preprocessed_data.csv
│   │   └── raw_extracted_data.csv
│   ├── data_output
│   │   └── calculated_steps.json
│   └── data_raw
│       └── 234 JSON files
├── docker-compose.yml
├── how_to_run.md
├── legacy_files
│   ├── create_sample_data.py
│   ├── feature_engineering.ipynb
│   ├── finding_height_peaks.py
│   ├── info.txt
│   ├── oop_steps_generator.py
│   └── steps_generator_function.py
├── models
│   └── random_forest_model.pkl
├── notebooks
│   ├── 1-data_preprocessing.ipynb
│   ├── 2-feature_engineering.ipynb
│   ├── 3-modeling.ipynb
│   ├── 4-pipeline.ipynb
│   └── snippets.ipynb
├── reports
│   ├── domain_knowledge_notes.md
│   └── notes.md
├── requirements.txt
├── src
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── steps_predictor.py
│   └── utils.py
└── tests
    ├── test_data_loader.py
    ├── test_data_processor.py
    ├── test_feature_extractor.py
    ├── test_step_prediction_pipeline.py
    └── test_steps_predictor.py
```

## 📦 Deliverables

### 🔹 Python Scripts / Jupyter Notebooks

- [Notebooks](https://github.com/arifhaidari/step_detection_data_science/tree/main/notebooks)
- [Step Calculation Scripts](https://github.com/arifhaidari/step_detection_data_science/blob/main/src)

### 🔹 Output Data

- [Calculated Steps JSON](https://github.com/arifhaidari/step_detection_data_science/tree/main/data/data_output)

### 🔹 Flutter Application for Data Visualization

- [Flutter Project](https://github.com/arifhaidari/step_detection_flutter/tree/main)

### 🔹 Documentation

- This README file
- Detailed documentation in the [Notebooks](https://github.com/arifhaidari/step_detection_data_science/tree/main/notebooks).

## 📊 Model Evaluation

Model evaluation details are documented in the following notebook:
🔗 [Modeling & Evaluation Notebook](https://github.com/arifhaidari/step_detection_data_science/blob/main/notebooks/3-modeling.ipynb)

## ⚠️ Challenges Encountered

- Understanding the sensor data and its structure.
- Effective feature engineering for accurate step count prediction.
- Exploring various sources to improve domain knowledge.

## 🔮 Future Improvements

- Implement deep learning models like **LSTM** or **Temporal CNN** for better temporal feature extraction.
- Improve real-time step classification instead of batch-based prediction.
- Enhance noise filtering techniques for more accurate step detection.

## 📚 References & Citations

The following sources were used for research and inspiration:

- [PMC: Step Detection Analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10187326/)
- [MDPI Sensors Research](https://www.mdpi.com/1424-8220/23/2/745)
- [Arxiv: Step Detection Using ML](https://arxiv.org/pdf/1801.02336)
- [Fraunhofer IIS - Gait Analysis](https://www.iis.fraunhofer.de/en/ff/sse/health/cic-gait-analysis-lab.html)
- [Women Who Code - Signal Processing](https://www.womenwhocode.com/blog/applications-of-signal-processing-in-machine-learning)
- [Medium: Low Pass Filtering](https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7)
- [GitHub: Step Detection ML](https://github.com/DidierRLopes/step-detection-ML/tree/main)
- [Feature Engineering Guide](https://medium.com/@rahulholla1/advanced-feature-engineering-for-time-series-data-5f00e3a8ad29)

---

**📌 Author:** Arif Haidari  
**🔗 GitHub:** [arifhaidari](https://github.com/arifhaidari)

Feel free to contribute, report issues, or suggest improvements!
🚀 Happy Coding!
