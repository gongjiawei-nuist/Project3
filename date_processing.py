import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


df = pd.read_csv("sensor_data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.set_index("Timestamp", inplace=True)


window_size = 3
df["Soil_Moisture_Denoised"] = df["Soil_Moisture"].rolling(window=window_size, center=True).mean()
df["Temperature_Denoised"] = df["Temperature"].rolling(window=window_size, center=True).mean()
df["Air_Humidity_Denoised"] = df["Air_Humidity"].rolling(window=window_size, center=True).mean()

df = df.dropna()

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(df[["Soil_Moisture_Denoised", "Temperature_Denoised", "Air_Humidity_Denoised"]])
scaled_df = pd.DataFrame(scaled_features, columns=["Soil_Moisture_Norm", "Temperature_Norm", "Air_Humidity_Norm"], index=df.index)

preprocessed_df = pd.concat([df, scaled_df], axis=1)

preprocessed_df.to_csv("preprocessed_data.csv")
print("Preprocessing complete. Saved to preprocessed_data.csv")

print("\nDescriptive Statistics (Denoised & Normalized):")
print(preprocessed_df.describe())
