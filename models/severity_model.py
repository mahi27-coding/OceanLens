import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

print("Model Comparison Started...")

# Load dataset
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

# Encode categorical features
df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
})

df["tourist_density"] = df["tourist_density"].fillna(1)
df["garbage_type"] = df["garbage_type"].fillna("mixed")
df["garbage_type"] = df["garbage_type"].astype("category").cat.codes

# Features & Target
X = df[["latitude", "longitude", "tourist_density", "garbage_type"]]
y = df["severity_level"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest Model
rf = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42
)
rf.fit(X_train, y_train)

print("\n=== FEATURE IMPORTANCE SECTION START ===")
importance = rf.feature_importances_
features = X.columns

print("\nFeature Importance Scores:")
for f, score in zip(features, importance):
    print(f, ":", round(score, 3))

rf_pred = rf.predict(X_test)

print("\nRandom Forest Accuracy:", accuracy_score(y_test, rf_pred))
print("\nRandom Forest Report:\n")
print(classification_report(y_test, rf_pred))

# Logistic Regression Model
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_pred = lr.predict(X_test)

print("\nLogistic Regression Accuracy:", accuracy_score(y_test, lr_pred))
print("\nLogistic Regression Report:\n")
print(classification_report(y_test, lr_pred))

# Cross Validation
rf_cv = cross_val_score(rf, X, y, cv=5)
print("\nRandom Forest Cross-Validation Accuracy:", rf_cv.mean())