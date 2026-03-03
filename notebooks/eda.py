import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/oceanlens_beach_observations_v1.csv")

print("Dataset Shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nSeverity Distribution:")
print(df["severity_level"].value_counts())

plt.figure(figsize=(6,4))
sns.countplot(x="severity_level", data=df)
plt.title("Severity Level Distribution")
plt.show()