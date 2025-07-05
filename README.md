# 🏦 Credit Risk Prediction Using Financial and Macroeconomic Data

## 📌 Project Overview

This project focuses on predicting the bankruptcy risk of companies using financial ratios and macroeconomic indicators. The goal is to build an interpretable and accurate machine learning model that helps stakeholders identify companies at high risk of default.

- ✅ Dataset: [Company Bankruptcy Prediction](https://www.kaggle.com/datasets/fedesoriano/company-bankruptcy-prediction)
- ✅ Model: XGBoost Classifier
- ✅ Explainability: SHAP values
- ✅ Output: Risk scoring and categorization (High, Medium, Low Risk)

---

## 🧠 Problem Statement

Predict whether a company is likely to go bankrupt based on its financial metrics. The model should also provide interpretability for each prediction to support financial decision-making.

---

## 📂 Folder Structure

```bash
Credit-Risk-Analysis/
│
├── data/
│   └── predicted_company_risk_scores.csv        # Exported predictions with risk levels
│
├── notebooks/
│   └── credit_risk_analysis.ipynb               # Jupyter notebook with full pipeline
│
├── visuals/
│   ├── shap_summary_plot.png                    # SHAP feature importance
│   └── risk_distribution.png                    # Risk score distribution
│
├── report/
│   └── project_summary.pdf                      # PDF report (optional)
│
└── README.md                                    # Project documentation
