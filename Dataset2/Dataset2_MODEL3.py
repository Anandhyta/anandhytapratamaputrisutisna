import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# =====================
# PATHS 
# =====================
data_path = "Data/dataset2_processed.csv"
model3_results = "Data/dataset2_model3_results"
os.makedirs(model3_results, exist_ok=True)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv(data_path)
print("===== DATA LOADED =====")
print(df.info())
print(df.head())

# =====================
# FEATURES & TARGET
# =====================
feature_columns = [
    "Age", "Income (USD)", "Rent (USD)", "Groceries (USD)", "Eating Out (USD)",
    "Entertainment (USD)", "Subscription Services (USD)", "Education (USD)",
    "Online Shopping (USD)", "Travel (USD)", "Fitness (USD)", "Miscellaneous (USD)"
]
target_column = "total_expense"

X = df[feature_columns]
y = df[target_column]

# =====================
# TRAIN-TEST SPLIT
# =====================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# =====================
# LINEAR REGRESSION
# =====================
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
y_pred_lin = lin_reg.predict(X_test)
mse_lin = mean_squared_error(y_test, y_pred_lin)
r2_lin = r2_score(y_test, y_pred_lin)
print(f"Linear Regression - MSE: {mse_lin:.2f}, R2: {r2_lin:.3f}")

# =====================
# RANDOM FOREST REGRESSION
# =====================
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"Random Forest Regression - MSE: {mse_rf:.2f}, R2: {r2_rf:.3f}")

# =====================
# FEATURE IMPORTANCE
# =====================
rf_feature_importance = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": rf_model.feature_importances_
}).sort_values(by="Importance", ascending=False)
rf_feature_importance.to_csv(os.path.join(model3_results, "RandomForest_Feature_Importance.csv"), index=False)
print(f"Feature importance saved to: {model3_results}")

# =====================
# SAVE PREDICTIONS
# =====================
predictions_df = pd.DataFrame({
    "ID": df.loc[y_test.index, "ID"],
    "Actual": y_test,
    "Pred_Linear": y_pred_lin,
    "Pred_RF": y_pred_rf
})

# FIX: rename Pred_RF menjadi overspending_risk
predictions_df = predictions_df.rename(columns={"Pred_RF": "overspending_risk"})
# pastikan tipe ID sama dengan dataframe lain
predictions_df['ID'] = predictions_df['ID'].astype(float)

predictions_df.to_csv(os.path.join(model3_results, "Budget_Forecasting_Predictions.csv"), index=False)
print(f"Predictions saved to: {model3_results}")

# =====================
# VISUALIZATIONS
# =====================
# 1. Actual vs Predicted
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred_lin, alpha=0.6, label="Linear Regression")
plt.scatter(y_test, y_pred_rf, alpha=0.6, label="Random Forest")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Actual Total Expense")
plt.ylabel("Predicted Total Expense")
plt.title("Actual vs Predicted - Budget Forecasting")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(model3_results, "Actual_vs_Predicted.png"))
plt.close()

# 2. Feature Importance (barplot)
plt.figure(figsize=(10,6))
sns.barplot(x="Importance", y="Feature", data=rf_feature_importance, palette="viridis")
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig(os.path.join(model3_results, "Feature_Importance.png"))
plt.close()

print("Visualizations saved to:", model3_results)
print("Model 3 (Budget Forecasting) training & evaluation completed successfully!")
