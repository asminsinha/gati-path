import pandas as pd
import numpy as np
import os

np.random.seed(42)

num_stops = 15

latitudes = np.random.uniform(12.90, 13.10, num_stops)
longitudes = np.random.uniform(77.50, 77.70, num_stops)

stop_names = [f"Stop_{i}" for i in range(num_stops)]

df = pd.DataFrame({
    'stop_name': stop_names,
    'latitude': latitudes,
    'longitude': longitudes,
    'demand_kg': np.random.randint(5, 50, num_stops) # Weight of package
})

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_path = os.path.join(base_dir, 'data', 'raw', 'bangalore_delivery_points.csv')

os.makedirs(os.path.dirname(save_path), exist_ok=True)

df.to_csv(save_path, index=False)

print("✅ Success! 'bangalore_delivery_points.csv' created in data/raw/")

print(df.head())