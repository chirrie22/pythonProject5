import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# 1. Fetch historical stock data (using Yahoo Finance for example)
stock_data = yf.download("AAPL", start="2024-01-01", end="2025-01-31")

# Reset the index to make the 'Date' a regular column
stock_data.reset_index(inplace=True)

# Display the first few rows of the stock data
print(stock_data.head())

# 2. Feature engineering
# For example, calculate a simple moving average (SMA) and handle missing values
stock_data['SMA_3'] = stock_data['Close'].rolling(window=3).mean()

# Fill missing values using forward fill
stock_data['SMA_3'] = stock_data['SMA_3'].ffill()

# Handle missing values using SimpleImputer for other columns (if needed)
imputer = SimpleImputer(strategy='mean')
stock_data_imputed = imputer.fit_transform(stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_3']])

# Convert imputed data back to DataFrame
stock_data_imputed = pd.DataFrame(stock_data_imputed, columns=['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_3'])
stock_data_imputed['Date'] = stock_data['Date']  # Keep the Date column as it is

print("Feature engineering completed!")
print(stock_data_imputed.head())

# 3. Prepare data for model training
X = stock_data_imputed[['Open', 'High', 'Low', 'Volume', 'SMA_3']]  # Features
y = stock_data_imputed['Close']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train and evaluate models

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
linear_predictions = linear_model.predict(X_test)
linear_mse = mean_squared_error(y_test, linear_predictions)
print(f'Linear Regression Mean Squared Error: {linear_mse}')

# Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)
rf_mse = mean_squared_error(y_test, rf_predictions)
print(f'Random Forest Mean Squared Error: {rf_mse}')

# Gradient Boosting Regressor
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)
gb_predictions = gb_model.predict(X_test)
gb_mse = mean_squared_error(y_test, gb_predictions)
print(f'Gradient Boosting Mean Squared Error: {gb_mse}')

# 5. Cross-Validation
# Perform cross-validation on the Random Forest model
rf_cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')
print(f'Random Forest Cross-Validation Mean Squared Error: {-rf_cv_scores.mean()}')

# Perform cross-validation on the Gradient Boosting model
gb_cv_scores = cross_val_score(gb_model, X, y, cv=5, scoring='neg_mean_squared_error')
print(f'Gradient Boosting Cross-Validation Mean Squared Error: {-gb_cv_scores.mean()}')