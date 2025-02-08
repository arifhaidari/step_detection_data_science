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
