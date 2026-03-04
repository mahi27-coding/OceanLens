import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("\nOceanLens Risk Prediction Model Starting...\n")

# -----------------------------
# Load dataset
# -----------------------------
try:
    df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")
except:
    print("Dataset not found.")
    exit()

print("Dataset Loaded Successfully\n")
print(df.head())

# -----------------------------
# Convert tourist density
# -----------------------------
df["tourist_density"] = df["tourist_density"].map({
    "Low": 0,
    "Medium": 1,
    "High": 2
})

# -----------------------------
# Features and Target
# -----------------------------
X = df[[
    "severity_level",
    "tourist_density"
]]

y = df["severity_level"]

# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Predictions
# -----------------------------
predictions = model.predict(X_test)

# -----------------------------
# Accuracy
# -----------------------------
accuracy = accuracy_score(y_test, predictions)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

# -----------------------------
# Example Prediction
# -----------------------------
sample = pd.DataFrame(
    [[2, 1]],
    columns=["severity_level", "tourist_density"]
)

prediction = model.predict(sample)

print("\nSample Prediction:")
print("Predicted Risk Level:", prediction[0])

print("\nOceanLens Risk Prediction Model Complete.\n")