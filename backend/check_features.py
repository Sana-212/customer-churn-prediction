import joblib
import os

model_path = os.path.join("..", "models", "model.pkl")
model = joblib.load(model_path)

# This prints the exact names the model needs
print(model.feature_names_in_)