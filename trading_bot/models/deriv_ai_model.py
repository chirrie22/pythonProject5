import joblib

model_path = r"C:\Users\chiri\PycharmProjects\pythonProject5\models\deriv_model.pkl"

try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
