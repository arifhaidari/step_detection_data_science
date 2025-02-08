# Step Detection - Data Science (under development)

source that I learned and inspired (citation):

https://pmc.ncbi.nlm.nih.gov/articles/PMC10187326/

https://www.mdpi.com/1424-8220/23/2/745

https://arxiv.org/pdf/1801.02336

https://www.iis.fraunhofer.de/en/ff/sse/health/cic-gait-analysis-lab.html

https://www.womenwhocode.com/blog/applications-of-signal-processing-in-machine-learning

https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7

https://github.com/DidierRLopes/step-detection-ML/tree/main

https://medium.com/@rahulholla1/advanced-feature-engineering-for-time-series-data-5f00e3a8ad29

https://machinelearningmastery.com/rfe-feature-selection-in-python/

https://medium.com/@salvarosacity/feature-engineering-based-on-sensory-data-9c98d7779156

Types of problem (Regression vs Classification):
it is a regression problem where using sensor data to predict the total number of steps → continuous numeric output so This is a regression problem because the target variable (step count) is a continuous value.

Based on my analysis it could be otherwise (classification) if instead of predicting the total count, you could classify each time frame as "step" or "no step".
or This could be a binary classification problem where the model learns step occurrences.
and it would be Useful if the goal is real-time detection, such as triggering alerts for unstable steps.

So, I go with regression problem where the goal is to provide a total step count per session

---

after feature engineering I only focused on how to count the steps.
However, if step patterns change over time due to user behavior, fatigue, or environment, then a time-aware model (LSTM, Temporal CNN, or ARIMA) might be needed. but current approach solve the problem of counting the steps in every measurement. it depends on the context and the problem we solve then definitely and time-aware models need to considered.

---

project structure:
.
├── README.md
├── app
│ └── info.txt
├── data
│ ├── calculated_steps.json
│ ├── feature_engineered_data.csv
│ ├── preprocessed_data.csv
│ └── raw_extracted_data.csv
├── fastapi
│ ├── config.py
│ ├── data_processing.py
│ ├── main.py
│ ├── model.py
│ └── utils.py
├── legacy_files
│ ├── feature_engineering.ipynb
│ └── info.txt
├── models
│ └── random_forest_model.pkl
├── notebooks
│ ├── 1-data_preprocessing.ipynb
│ ├── 2-feature_engineering.ipynb
│ ├── 3-modeling.ipynb
│ ├── 4-pipeline.ipynb
│ └── alternatives.ipynb
├── raw_data
│ └── 234 json file
├── report
│ ├── domain_knowledge_notes.md
│ └── notes.md
├── requirements.txt
├── src
│ ├── calculated_steps_generator.py
│ ├── create_sample_data.py
│ ├── finding_height_peaks.py
│ └── utils.py
└── template.config.js

---

Deliverables:
in this project I was asked to present the following

1. A Python script or Jupyter Notebook implementing the step detection model.
   https://github.com/arifhaidari/step_detection_data_science/tree/main/notebooks
   https://github.com/arifhaidari/step_detection_data_science/blob/main/src/calculated_steps_generator.py

2. The calculated_steps.json file containing the results.
   https://github.com/arifhaidari/step_detection_data_science/blob/main/data/calculated_steps.json

3. A Flutter project with the data visualization app.
   link flutter project and also the app
   https://github.com/arifhaidari/step_detection_data_science/tree/main/app

4. A brief documentation (Markdown or PDF):
   this README.md file

   The approach used for both ML and Flutter components:
   for the flutter approaches i refer you to the flutter project (link).
   for my approaches for ML i refer you to the notebooks where every thing is documented step by step.
   https://github.com/arifhaidari/step_detection_data_science/tree/main/notebooks

   Challenges encountered:
   the challenging part for me was to familiarize myself with data and do the feature engineering. worth to mention going through and reading some articles, papers and projects in order get the knowledge.

   Model evaluation results:
   for this i refer you to the following notebook. you will find a exauhstive information in this regard.
   https://github.com/arifhaidari/step_detection_data_science/blob/main/notebooks/3-modeling.ipynb
