import pandas as pd
import numpy as np
import os

# 1. Create a "Seed" so the random numbers are the same every time we run it
np.random.seed(42)

# 2. Define how many delivery points we want
num_stops = 15

# 3. Simulate Latitude and Longitude for a city (Approx Bangalore coordinates)
# Bangalore is roughly Lat 12.97, Lon 77.59
latitudes = np.random.uniform(12.90, 13.10, num_stops)
longitudes = np.random.uniform(77.50, 77.70, num_stops)

# 4. Create a list of Stop Names
stop_names = [f"Stop_{i}" for i in range(num_stops)]

# 5. Put it all into a Table (DataFrame)
df = pd.DataFrame({
    'stop_name': stop_names,
    'latitude': latitudes,
    'longitude': longitudes,
    'demand_kg': np.random.randint(5, 50, num_stops) # Weight of package
})

# 6. Save this to your data/raw folder
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_path = os.path.join(base_dir, 'data', 'raw', 'bangalore_delivery_points.csv')

# Ensure the directory exists just in case
os.makedirs(os.path.dirname(save_path), exist_ok=True)

df.to_csv(save_path, index=False)

print("✅ Success! 'bangalore_delivery_points.csv' created in data/raw/")

print(df.head()) # Show the first few rows