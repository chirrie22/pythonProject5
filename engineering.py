import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Load your data
data = {
    'Date': ['2024-12-03', '2024-12-04', '2024-12-05', '2024-12-06', '2024-12-09'],
    'Open': [242.649994, 243.009995, 243.039993, 242.839996, 246.750000],
    'High': [242.759995, 244.110001, 244.539993, 244.630005, 247.240005],
    'Low': [241.419998, 242.570007, 242.729996, 242.470001, 241.630005],
    'Close': [239.809998, 242.869995, 243.990005, 242.910004, 241.830002],
    'Volume': [38861000, 44383900, 40033900, 36870600, 44649200],
    'SMA_3': [None, None, 242.223333, 243.256668, 242.910004]
}

df = pd.DataFrame(data)
print("Data loaded successfully!")

# Feature engineering - fill missing values for the SMA_3 column
print(f"Rows before feature engineering: {len(df)}")
df['SMA_3'] = df['SMA_3'].ffill()  # Forward fill missing values
print(f"Rows after feature engineering: {len(df)}")

# Handle missing values in the entire dataset using SimpleImputer
imputer = SimpleImputer(strategy='mean')  # You can use 'median' or 'most_frequent' as well
df_imputed = imputer.fit_transform(df[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_3']])

# Convert imputed data back to DataFrame
df_imputed = pd.DataFrame(df_imputed, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_3'])
df_imputed['Date'] = df['Date']  # Keep the Date column as it is

print("Feature engineering completed!")
print(df_imputed.head())

# Prepare data for model training
X = df_imputed[['Open', 'High', 'Low', 'Volume', 'SMA_3']]  # Features
y = df_imputed['Close']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
try:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
except Exception as e:
    print(f"Error during model training and prediction: {e}")