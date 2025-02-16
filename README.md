# Step Detection - Data Science

## How to run?

before we start, if you want to run first, here is a step by step guid how to run the project and try everything by yourself and get hands on experience - the link: <br>
https://github.com/arifhaidari/step_detection_data_science/blob/main/how_to_run.md

## Introduction

This project is developed as part of a task assigned by EVERSION Technologies GmbH to evaluate my data science skills. The objective is to build a step detection model using sensor data and apply machine learning techniques to predict the total number of steps taken in a session.

## Problem Definition

Step detection is an essential component in various applications, including fitness tracking, rehabilitation, and gait analysis. The goal of this project is to predict the total number of steps from sensor data.

- **Type of problem:** Regression
- **Why Regression?** Since the goal is to predict the total step count (a continuous numerical value), this is a regression problem.
- **Alternative Approach:** It could be framed as a classification problem if the goal was to classify each time frame as "step" or "no step," useful for real-time detection.

## Approach

1. **Data Preprocessing:**

   - Handling missing values and noise reduction using filtering techniques.
   - Extracting features from raw sensor data.

2. **Feature Engineering:**

   - Analyzing sensor signals to derive meaningful features.
   - Evaluating feature importance for step count prediction.

3. **Modeling:**

   - Implemented a **Random Forest model** for step count prediction.
   - Evaluated different machine learning models to optimize performance.

4. **Evaluation & Deployment:**
   - Analyzed model performance.
   - Packaged the model using FastAPI.
   - Provided a Flutter-based visualization app.

## Project Structure

```
.
├── Dockerfile
├── README.md
├── app
│   └── download_app.txt
├── data
│   ├── calculated_steps.json
│   ├── feature_engineered_data.csv
│   ├── preprocessed_data.csv
│   └── raw_extracted_data.csv
├── docker-compose.yml
├── fastapi
│   ├── config.py
│   ├── data_processing.py
│   ├── main.py
│   ├── models.py
│   ├── predict_step.py
│   └── utils.py
├── legacy_files
│   ├── feature_engineering.ipynb
│   └── info.txt
├── models
│   └── random_forest_model.pkl
├── notebooks
│   ├── 1-data_preprocessing.ipynb
│   ├── 2-feature_engineering.ipynb
│   ├── 3-modeling.ipynb
│   ├── 4-pipeline.ipynb
│   └── alternatives.ipynb
├── raw_data
│   └── 234 json file
├── reports
│   ├── domain_knowledge_notes.md
│   └── notes.md
├── requirements.txt
└── src
    ├── calculated_steps_generator.py
    ├── create_sample_data.py
    ├── finding_height_peaks.py
    └── utils.py
```

## Deliverables

The project includes the following key deliverables:

1. **Python Script / Jupyter Notebook** implementing step detection:

   - [Notebooks](https://github.com/arifhaidari/step_detection_data_science/tree/main/notebooks)
   - [Step Calculation Script](https://github.com/arifhaidari/step_detection_data_science/blob/main/src/calculated_steps_generator.py)

2. **Output Data:**

   - [Calculated Steps JSON](https://github.com/arifhaidari/step_detection_data_science/blob/main/data/calculated_steps.json)

3. **Flutter Application for Data Visualization:**

   - [Flutter Project](https://github.com/arifhaidari/step_detection_flutter/tree/main)

4. **Documentation (Markdown/PDF):**
   - This README file
   - Detailed documentation in the [Notebooks](https://github.com/arifhaidari/step_detection_data_science/tree/main/notebooks).

## Model Evaluation

Model evaluation details are documented in the following notebook:

- [Modeling & Evaluation Notebook](https://github.com/arifhaidari/step_detection_data_science/blob/main/notebooks/3-modeling.ipynb)

## Challenges Encountered

- Understanding the sensor data and its structure.
- Effective feature engineering for accurate step count prediction.
- Exploring various sources to improve domain knowledge.

## References & Citations

The following sources were used for research and inspiration:

- [PMC: Step Detection Analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10187326/)
- [MDPI Sensors Research](https://www.mdpi.com/1424-8220/23/2/745)
- [Arxiv: Step Detection Using ML](https://arxiv.org/pdf/1801.02336)
- [Fraunhofer IIS - Gait Analysis](https://www.iis.fraunhofer.de/en/ff/sse/health/cic-gait-analysis-lab.html)
- [Women Who Code - Signal Processing](https://www.womenwhocode.com/blog/applications-of-signal-processing-in-machine-learning)
- [Medium: Low Pass Filtering](https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7)
- [GitHub: Step Detection ML](https://github.com/DidierRLopes/step-detection-ML/tree/main)
- [Feature Engineering Guide](https://medium.com/@rahulholla1/advanced-feature-engineering-for-time-series-data-5f00e3a8ad29)

## Future Improvements

- Implement deep learning models like **LSTM** or **Temporal CNN** for better temporal feature extraction.
- Improve real-time step classification instead of batch-based prediction.
- Enhance noise filtering techniques for more accurate step detection.
