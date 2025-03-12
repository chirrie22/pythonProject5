import joblib
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

# Ensure the "models" directory exists
models_dir = "C:/Users/chiri/PycharmProjects/pythonProject5/models"
os.makedirs(models_dir, exist_ok=True)  # Create if it doesn't exist

# Generate dummy training data
X_train = np.random.rand(100, 3)  # Example: [price, SMA_10, RSI]
y_train = np.random.choice([0, 1], 100)  # 0 = PUT, 1 = CALL

# Train the model
model = RandomForestClassifier(n_estimators=10)
model.fit(X_train, y_train)

# Save the trained model
model_path = os.path.join(models_dir, "deriv_model.pkl")
joblib.dump(model, model_path)

print(f"✅ Model saved successfully at {model_path}!")
