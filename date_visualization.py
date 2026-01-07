import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv("preprocessed_data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.set_index("Timestamp", inplace=True)

plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

axes[0].plot(df.index, df["Soil_Moisture_Denoised"], color="green", label="Denoised Soil Moisture")
axes[0].set_ylabel("Soil Moisture (0-1023)")
axes[0].set_title("Soil Moisture Trend Over Time")
axes[0].legend()


axes[1].plot(df.index, df["Temperature_Denoised"], color="red", label="Denoised Temperature")
axes[1].set_ylabel("Temperature (°C)")
axes[1].set_title("Temperature Trend Over Time")
axes[1].legend()


axes[2].plot(df.index, df["Air_Humidity_Denoised"], color="blue", label="Denoised Air Humidity")
axes[2].set_ylabel("Air Humidity (%)")
axes[2].set_xlabel("Time")
axes[2].set_title("Air Humidity Trend Over Time")
axes[2].legend()

axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
axes[2].xaxis.set_major_locator(mdates.HourLocator(interval=6))
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("time_series_trends.png", dpi=300, bbox_inches="tight")
plt.show()

print("Key Descriptive Statistics:")
stats = df[["Soil_Moisture_Denoised", "Temperature_Denoised", "Air_Humidity_Denoised"]].agg(["mean", "std", "min", "max"])
print(stats)
