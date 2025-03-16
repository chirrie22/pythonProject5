import joblib
import os

# Absolute path resolution
model_path = os.path.join(os.path.dirname(__file__), "..", "..", "models", "deriv_model.pkl")

# Load the model
model = joblib.load(model_path)
