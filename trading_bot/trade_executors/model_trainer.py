import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from .feature_engineering import add_features


def train_model():
    # Load historical data
    df = pd.read_csv('historical_ticks.csv')
    # Feature engineering
    df = add_features(df)

    # Define features and target
    features = ['MA_5', 'MA_20', 'RSI', 'upper_band', 'lower_band']
    X = df[features]
    y = df['target']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

    # Save the model to a file
    joblib.dump(model, 'models/deriv_model.pkl')


if __name__ == '__main__':
    train_model()
