import pandas as pd

# Load the dataset
data = pd.read_csv('deriv_v75_data.csv')

# Check if the file exists
print("File exists!")

# Preview the first few rows of the data
print("First few rows of the data:")
print(data.head())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Fill missing values with the mean of each column (only for numeric columns)
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Print the first few rows after filling missing values
print("\nFirst few rows after filling missing values:")
print(data.head())
