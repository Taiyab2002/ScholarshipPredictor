import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================
# 1. Load Dataset
# ==========================================

data = pd.read_csv(
    "dataset/higher_study_scholarship_dataset.csv"
)

print("\nDataset loaded successfully!")
print("Dataset shape:", data.shape)

# ==========================================
# 2. Separate Features and Target
# ==========================================

target_column = "scholarship_eligible"

X = data.drop(columns=[target_column])
y = data[target_column]

print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print(target_column)

# ==========================================
# 3. Identify Numerical and Categorical Data
# ==========================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    exclude=["object"]
).columns.tolist()

print("\nCategorical columns:")
print(categorical_columns)

print("\nNumerical columns:")
print(numerical_columns)

# ==========================================
# 4. Preprocessing
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)

# ==========================================
# 5. Create ML Model
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

# ==========================================
# 6. Create Pipeline
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# ==========================================
# 7. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ==========================================
# 8. Train Model
# ==========================================

print("\nTraining Random Forest model...")

pipeline.fit(X_train, y_train)

print("Model training completed!")

# ==========================================
# 9. Make Predictions
# ==========================================

y_pred = pipeline.predict(X_test)

# ==========================================
# 10. Calculate Model Performance
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    pos_label="Yes"
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label="Yes"
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label="Yes"
)

print("\n==========================================")
print("MODEL PERFORMANCE")
print("==========================================")

print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall   : {recall * 100:.2f}%")
print(f"F1 Score : {f1 * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ==========================================
# 11. Feature Importance
# ==========================================

print("\n==========================================")
print("FEATURE IMPORTANCE")
print("==========================================")

# Get the fitted preprocessing component
fitted_preprocessor = pipeline.named_steps["preprocessor"]

# Get encoded feature names
encoded_feature_names = (
    fitted_preprocessor
    .get_feature_names_out()
)

# Get Random Forest model
random_forest = pipeline.named_steps["model"]

# Get importance values
importance_values = random_forest.feature_importances_

# Create DataFrame
feature_importance = pd.DataFrame({
    "feature": encoded_feature_names,
    "importance": importance_values
})

# Sort from highest to lowest
feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("\nTop 15 Important Features:")

print(
    feature_importance.head(15).to_string(index=False)
)

# ==========================================
# 12. Save Feature Importance
# ==========================================

feature_importance.to_json(
    "feature_importance.json",
    orient="records",
    indent=4
)

print("\nFeature importance saved as:")
print("feature_importance.json")

# ==========================================
# 13. Save Model Performance
# ==========================================

performance = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "training_samples": len(X_train),
    "testing_samples": len(X_test),
    "dataset_size": len(data),
    "algorithm": "Random Forest Classifier"
}

with open(
    "model_performance.json",
    "w"
) as file:

    json.dump(
        performance,
        file,
        indent=4
    )

print("\nModel performance saved as:")
print("model_performance.json")

# ==========================================
# 14. Save Trained Model
# ==========================================

joblib.dump(
    pipeline,
    "scholarship_model.pkl"
)

print("\n==========================================")
print("SUCCESS!")
print("==========================================")

print("Model saved as: scholarship_model.pkl")
print("Feature importance saved as: feature_importance.json")
print("Performance saved as: model_performance.json")