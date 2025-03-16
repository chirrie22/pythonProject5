import pandas as pd
import os

# Define file path
data_path = os.path.join(os.path.dirname(__file__), "data.csv")

# Sample price data
data = {
    "date": ["2025-03-10", "2025-03-11", "2025-03-12", "2025-03-13", "2025-03-14"],
    "price": [100, 102, 99, 105, 98]
}

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv(data_path, index=False)

print(f"Sample data.csv created successfully at {data_path}!")
