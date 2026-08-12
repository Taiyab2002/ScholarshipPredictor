import pandas as pd
import joblib
import json

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


# ==========================================
# SMARTSCHOLAR - MODEL TRAINING PIPELINE
# ==========================================


# ==========================================
# FILE PATHS
# ==========================================

DATASET_PATH = "dataset/higher_study_scholarship_dataset.csv"
MODEL_PATH = "scholarship_model.pkl"
PERFORMANCE_PATH = "model_performance.json"
COMPARISON_PATH = "model_comparison.csv"
FEATURE_IMPORTANCE_PATH = "feature_importance.json"


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv(DATASET_PATH)

print("\n==========================================")
print("SMARTSCHOLAR MODEL TRAINING")
print("==========================================")

print("\nDataset loaded successfully!")
print("Dataset shape:", data.shape)


# ==========================================
# 2. SEPARATE FEATURES AND TARGET
# ==========================================

target_column = "scholarship_eligible"

X = data.drop(columns=[target_column])
y = data[target_column]


print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print(target_column)


# ==========================================
# 3. IDENTIFY DATA TYPES
# ==========================================

# Explicitly use "str" to avoid the pandas
# select_dtypes compatibility warning.

categorical_columns = X.select_dtypes(
    include=["str"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    exclude=["str"]
).columns.tolist()


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumerical columns:")
print(numerical_columns)


# ==========================================
# 4. TRAIN / TEST SPLIT
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
# 5. PREPROCESSORS
# ==========================================

# ------------------------------------------
# Common preprocessing
# ------------------------------------------

common_preprocessor = ColumnTransformer(
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


# ------------------------------------------
# Logistic Regression preprocessing
# ------------------------------------------
# Numerical features are standardized
# because Logistic Regression benefits
# from feature scaling.

logistic_preprocessor = ColumnTransformer(
    transformers=[

        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),

        (
            "numerical",
            StandardScaler(),
            numerical_columns
        )
    ]
)


# ==========================================
# 6. DEFINE MULTIPLE ML MODELS
# ==========================================

models = {

    # ======================================
    # MODEL 1
    # LOGISTIC REGRESSION
    # L2 REGULARIZATION
    # ======================================

    "Logistic Regression (L2 Regularization)":

        Pipeline(
            steps=[

                (
                    "preprocessor",
                    logistic_preprocessor
                ),

                (
                    "model",
                    LogisticRegression(

                        # Explicit L2 regularization
                        penalty="l2",

                        # Regularization strength
                        C=1.0,

                        max_iter=2000,

                        random_state=42
                    )
                )
            ]
        ),


    # ======================================
    # MODEL 2
    # DECISION TREE
    # ======================================

    "Decision Tree":

        Pipeline(
            steps=[

                (
                    "preprocessor",
                    common_preprocessor
                ),

                (
                    "model",
                    DecisionTreeClassifier(

                        max_depth=5,

                        min_samples_split=10,

                        min_samples_leaf=4,

                        random_state=42
                    )
                )
            ]
        ),


    # ======================================
    # MODEL 3
    # RANDOM FOREST
    # ======================================

    "Random Forest":

        Pipeline(
            steps=[

                (
                    "preprocessor",
                    common_preprocessor
                ),

                (
                    "model",
                    RandomForestClassifier(

                        n_estimators=200,

                        max_depth=8,

                        min_samples_split=5,

                        min_samples_leaf=2,

                        random_state=42
                    )
                )
            ]
        )
}


# ==========================================
# 7. TRAIN AND EVALUATE MODELS
# ==========================================

results = []

trained_models = {}


print("\n==========================================")
print("MODEL TRAINING & EVALUATION")
print("==========================================")


for model_name, pipeline in models.items():

    print(f"\nTraining {model_name}...")

    # --------------------------------------
    # Train model
    # --------------------------------------

    pipeline.fit(
        X_train,
        y_train
    )


    # --------------------------------------
    # Make predictions
    # --------------------------------------

    y_pred = pipeline.predict(
        X_test
    )


    # --------------------------------------
    # Calculate metrics
    # --------------------------------------

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        pos_label="Yes",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        pos_label="Yes",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        pos_label="Yes",
        zero_division=0
    )


    # --------------------------------------
    # Store results
    # --------------------------------------

    results.append({

        "model":
            model_name,

        "accuracy":
            round(
                accuracy * 100,
                2
            ),

        "precision":
            round(
                precision * 100,
                2
            ),

        "recall":
            round(
                recall * 100,
                2
            ),

        "f1_score":
            round(
                f1 * 100,
                2
            )
    })


    # Store trained pipeline

    trained_models[
        model_name
    ] = pipeline


    # --------------------------------------
    # Display model results
    # --------------------------------------

    print(
        f"Accuracy : {accuracy * 100:.2f}%"
    )

    print(
        f"Precision: {precision * 100:.2f}%"
    )

    print(
        f"Recall   : {recall * 100:.2f}%"
    )

    print(
        f"F1 Score : {f1 * 100:.2f}%"
    )


# ==========================================
# 8. CREATE MODEL COMPARISON
# ==========================================

comparison = pd.DataFrame(
    results
)


# ------------------------------------------
# Sort models
# ------------------------------------------
# Primary criterion:
# F1 Score
#
# Secondary criterion:
# Accuracy

comparison = comparison.sort_values(

    by=[
        "f1_score",
        "accuracy"
    ],

    ascending=False

).reset_index(
    drop=True
)


# ------------------------------------------
# Add ranking
# ------------------------------------------

comparison.insert(

    0,

    "rank",

    range(
        1,
        len(comparison) + 1
    )
)


print("\n==========================================")
print("FINAL MODEL COMPARISON")
print("==========================================")


print(
    comparison.to_string(
        index=False
    )
)


# ==========================================
# SAVE MODEL COMPARISON
# ==========================================

comparison.to_csv(

    COMPARISON_PATH,

    index=False
)


# ==========================================
# 9. SELECT BEST MODEL
# ==========================================

best_model_name = comparison.iloc[0]["model"]


best_pipeline = trained_models[
    best_model_name
]


best_result = comparison.iloc[0].to_dict()


print("\n==========================================")
print("BEST MODEL")
print("==========================================")

print(
    "Best model:",
    best_model_name
)

print(
    "Selection metric: F1 Score"
)


# ==========================================
# 10. CLASSIFICATION REPORT
# ==========================================

best_predictions = best_pipeline.predict(
    X_test
)


print("\n==========================================")
print("BEST MODEL CLASSIFICATION REPORT")
print("==========================================")


print(
    classification_report(
        y_test,
        best_predictions,
        zero_division=0
    )
)


# ==========================================
# 11. RANDOM FOREST FEATURE IMPORTANCE
# ==========================================

if "Random Forest" in best_model_name:

    # --------------------------------------
    # Get fitted preprocessor
    # --------------------------------------

    fitted_preprocessor = (

        best_pipeline
        .named_steps["preprocessor"]

    )


    # --------------------------------------
    # Get transformed feature names
    # --------------------------------------

    feature_names = (

        fitted_preprocessor
        .get_feature_names_out()

    )


    # --------------------------------------
    # Get Random Forest model
    # --------------------------------------

    random_forest = (

        best_pipeline
        .named_steps["model"]

    )


    # --------------------------------------
    # Get feature importance values
    # --------------------------------------

    importance_values = (

        random_forest
        .feature_importances_

    )


    # --------------------------------------
    # Create feature importance table
    # --------------------------------------

    feature_importance = pd.DataFrame({

        "feature":
            feature_names,

        "importance":
            importance_values

    })


    # Sort highest to lowest

    feature_importance = (

        feature_importance
        .sort_values(
            by="importance",
            ascending=False
        )

    )


    # --------------------------------------
    # Save feature importance
    # --------------------------------------

    feature_importance.to_json(

        FEATURE_IMPORTANCE_PATH,

        orient="records",

        indent=4

    )


    print(
        "\nFeature importance saved as:",
        FEATURE_IMPORTANCE_PATH
    )


# ==========================================
# 12. SAVE MODEL PERFORMANCE
# ==========================================

performance = {

    "best_model":
        best_model_name,

    "selection_metric":
        "F1 Score",

    "accuracy":
        best_result["accuracy"],

    "precision":
        best_result["precision"],

    "recall":
        best_result["recall"],

    "f1_score":
        best_result["f1_score"],

    "training_samples":
        len(X_train),

    "testing_samples":
        len(X_test),

    "dataset_size":
        len(data),

    "models_evaluated":
        comparison["model"].tolist(),

    "regularization":
        "L2 Regularization in Logistic Regression",

    "logistic_regression_parameters": {

        "penalty":
            "l2",

        "C":
            1.0
    }
}


with open(

    PERFORMANCE_PATH,

    "w"

) as file:

    json.dump(

        performance,

        file,

        indent=4

    )


# ==========================================
# 13. SAVE BEST MODEL
# ==========================================

joblib.dump(

    best_pipeline,

    MODEL_PATH

)


# ==========================================
# 14. FINAL SUMMARY
# ==========================================

print("\n==========================================")
print("TRAINING SUMMARY")
print("==========================================")

print(
    f"Dataset size    : {len(data)}"
)

print(
    f"Training samples: {len(X_train)}"
)

print(
    f"Testing samples : {len(X_test)}"
)

print(
    f"Models evaluated: {len(models)}"
)

print(
    f"Best model      : {best_model_name}"
)

print(
    f"Best F1 Score   : {best_result['f1_score']:.2f}%"
)

print(
    f"Best Accuracy   : {best_result['accuracy']:.2f}%"
)

print(
    "Regularization  : L2"
)


# ==========================================
# 15. OUTPUT FILES
# ==========================================

print("\n==========================================")
print("OUTPUT FILES")
print("==========================================")

print(
    "Best model saved as:",
    MODEL_PATH
)

print(
    "Model comparison saved as:",
    COMPARISON_PATH
)

print(
    "Performance saved as:",
    PERFORMANCE_PATH
)

print(
    "Feature importance saved as:",
    FEATURE_IMPORTANCE_PATH
)


print("\n==========================================")
print("SUCCESS!")
print("==========================================")

print(
    "Training pipeline completed successfully!"
)