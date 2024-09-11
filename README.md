# Stock Trend Prediction using Technical Indicator and News Sentiment Analysis with FinBERT

#   Overview

This repository contains a Jupyter Notebook that performs machine learning analysis on financial data. The notebook demonstrates data preprocessing, model training, and evaluation of several classifiers including Logistic Regression, Random Forest, and Gradient Boosting.  

## Notebook Contents

    Data Preparation
        Importing Data: The notebook starts by importing necessary libraries and the dataset.
        Train-Test Split: The dataset is split into training and testing sets with the following shapes:
            Training set: (2039, 6)
            Testing set: (252, 6)

    Model Training and Evaluation
        Logistic Regression
            Training Accuracy: 53.85%
            Testing Accuracy: 53.17%
            Notable Metrics: Precision and recall issues with class 0.
        Random Forest
            Training Accuracy: 54.73%
            Testing Accuracy: 53.57%
            Notable Metrics: Higher precision for class 0 but lower recall.
        Gradient Boosting
            Training Accuracy: 70.48%
            Testing Accuracy: 52.38%
            Notable Metrics: Better performance in training but lower testing accuracy.

## Model Performance

    Logistic Regression:
        Overall Accuracy: 61%
        Uptrend Accuracy: 58%
        Downtrend Accuracy: 66%

    Random Forest:
        Overall Accuracy: 63%
        Uptrend Accuracy: 61%
        Downtrend Accuracy: 68%

    Gradient Boosting:
        Overall Accuracy: 61%
        Uptrend Accuracy: 59%
        Downtrend Accuracy: 63%

# Usage

To replicate the analysis, clone the repository and run the model.ipynb notebook in a Jupyter environment. Ensure all required libraries are installed.