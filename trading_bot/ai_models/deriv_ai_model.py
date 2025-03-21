import joblib
import numpy as np

class DerivAIModel:
    def __init__(self, model_path="C:/Users/chiri/PycharmProjects/pythonProject5/models/deriv_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            self.model = joblib.load(self.model_path)
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")

    def predict(self, data):
        if self.model is None:
            raise ValueError("Model not loaded.")

        # Ensure correct input shape
        data = np.array(data).reshape(1, -1)

        if data.shape[1] != self.model.n_features_in_:
            raise ValueError(f"Model expects {self.model.n_features_in_} features, but got {data.shape[1]}.")

        return self.model.predict(data)
