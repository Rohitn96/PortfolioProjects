# Customer Churn Prediction Model

This project aims to predict customer churn using various machine learning and deep learning techniques. The goal is to help businesses understand the factors contributing to customer attrition and take proactive measures to retain customers.

## Data
The dataset used in this project can be found in the data/ folder. It includes customer information such as demographics, account details, and service usage.

## Dataset Features
CustomerID: Unique identifier for each customer
Gender: Gender of the customer
Age: Age of the customer
Tenure: Number of months the customer has been with the company
ServiceUsage: Various metrics indicating the usage of services
Churn: Target variable indicating whether the customer has churned (1) or not (0)
Modeling
This project utilizes both machine learning and deep learning models to predict customer churn. The key steps include:

## Data Preprocessing: Cleaning and preparing the data for modeling.
Feature Engineering: Creating relevant features that can improve model performance.
Model Training: Using scikit-learn for traditional models and TensorFlow and Keras for deep learning.
Model Evaluation: Evaluating the models using performance metrics like accuracy, ROC curve, and confusion matrix.
Libraries and Techniques Used
scikit-learn: For Logistic Regression, Random Forest, and model evaluation.
TensorFlow and Keras: For building and training Neural Networks.
Matplotlib and Seaborn: For visualizing the results and metrics.

## Evaluation
The performance of the models is evaluated using the following metrics:

Confusion Matrix: Visual representation of true vs. predicted values.
ROC Curve: Graphical plot to evaluate the trade-off between true positive rates and false positive rates.
AUC Score: Area Under the ROC Curve, indicating model performance.

## Results
The results showcase which model performs best for predicting customer churn. The ROC curve and confusion matrix provide insights into the model's accuracy and effectiveness.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
