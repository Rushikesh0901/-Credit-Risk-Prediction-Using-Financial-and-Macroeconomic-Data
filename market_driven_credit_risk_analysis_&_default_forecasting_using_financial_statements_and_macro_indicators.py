# -*- coding: utf-8 -*-
"""Market-Driven Credit Risk Analysis & Default Forecasting Using Financial Statements and Macro Indicators.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fj5dfw7bbjZ6URa0XZ8sCh50grwNFkeU
"""

#Step 1: Import Required Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
from xgboost import XGBClassifier
import shap
import warnings
warnings.filterwarnings("ignore")

# ✅ Step 2: Load Bankruptcy Dataset from Kaggle input folder (no zip needed)
import pandas as pd

# Path to mounted dataset (Kaggle notebook environment)
csv_file = "/kaggle/input/company-bankruptcy-prediction/data.csv"

# Load the dataset
data = pd.read_csv(csv_file)

# Display basic info
print("✅ Dataset loaded successfully!")
print("Shape of Dataset:", data.shape)
print(data.head())

# 📊 Step 3: Check for Nulls and Data Types
print("\nMissing values:")
print(data.isnull().sum())
print("\nData types:")
print(data.dtypes)

# 🎯 Step 4: Define Features and Target
X = data.drop('Bankrupt?', axis=1)
y = data['Bankrupt?']

# 📐 Step 5: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# ⚖️ Step 6: Normalize Features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 🤖 Step 7: Train XGBoost Model
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train_scaled, y_train)

# 📈 Step 8: Evaluate the Model
y_pred = model.predict(X_test_scaled)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nROC-AUC Score:", roc_auc_score(y_test, y_pred))

# 🔍 Step 9: SHAP Explainability
explainer = shap.Explainer(model)
shap_values = explainer(X_test_scaled)

# Plot summary of feature importance
shap.summary_plot(shap_values, X_test, plot_type="bar")

# 📊 Step 10: Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# 📌 Step 11: Save Risk Scores for Companies
risk_scores = model.predict_proba(X_test_scaled)[:, 1]
risk_df = pd.DataFrame({
    'Company_ID': X_test.index,
    'Risk_Score': risk_scores,
    'Actual_Status': y_test.values,
    'Predicted_Status': y_pred
})
risk_df.sort_values('Risk_Score', ascending=False, inplace=True)
print("\nTop High-Risk Companies:")
print(risk_df.head(10))

# Distribution of Risk Scores
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.histplot(risk_df['Risk_Score'], bins=30, kde=True, color='crimson')
plt.title("Distribution of Predicted Credit Risk Scores")
plt.xlabel("Risk Score (Probability of Bankruptcy)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()

# Categorize companies by risk level
def risk_category(score):
    if score >= 0.75:
        return 'High Risk'
    elif score >= 0.5:
        return 'Medium Risk'
    else:
        return 'Low Risk'

risk_df['Risk_Level'] = risk_df['Risk_Score'].apply(risk_category)

# Summary of categories
print("\nRisk Category Summary:")
print(risk_df['Risk_Level'].value_counts())

plt.figure(figsize=(8, 5))
sns.countplot(data=risk_df, x='Risk_Level', palette='Set2', order=['High Risk', 'Medium Risk', 'Low Risk'])
plt.title("Company Risk Level Counts")
plt.xlabel("Risk Category")
plt.ylabel("Number of Companies")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Save to CSV for dashboard or reporting
risk_df.to_csv("predicted_company_risk_scores.csv", index=False)
print("✅ Risk scores exported to 'predicted_company_risk_scores.csv'")

# Summary metrics
summary = {
    'Model': ['XGBoost'],
    'Accuracy': [round((y_test == y_pred).mean(), 3)],
    'ROC-AUC': [round(roc_auc_score(y_test, y_pred), 3)],
    'High Risk Companies (>75%)': [sum(risk_df['Risk_Level'] == 'High Risk')],
    'Medium Risk Companies (50-75%)': [sum(risk_df['Risk_Level'] == 'Medium Risk')],
    'Low Risk Companies (<50%)': [sum(risk_df['Risk_Level'] == 'Low Risk')],
}

summary_df = pd.DataFrame(summary)
print("📈 Executive Summary:")
print(summary_df)

