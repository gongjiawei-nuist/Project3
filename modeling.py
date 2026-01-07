import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")
df = pd.read_csv("preprocessed_data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.set_index("Timestamp", inplace=True)


X = df[["Temperature_Norm", "Air_Humidity_Norm"]].values
y = df["Soil_Moisture_Norm"].values


train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]


lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)


mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)
print("Linear Regression Performance:")
print(f"MSE: {mse_lr:.4f}, R²: {r2_lr:.4f}")

def create_sequences(X, y, time_steps=3):
    X_seq, y_seq = [], []
    for i in range(len(X) - time_steps):
        X_seq.append(X[i:i+time_steps])
        y_seq.append(y[i+time_steps])
    return np.array(X_seq), np.array(y_seq)

time_steps = 3
X_train_seq, y_train_seq = create_sequences(X_train, y_train, time_steps)
X_test_seq, y_test_seq = create_sequences(X_test, y_test, time_steps)

lstm_model = Sequential()
lstm_model.add(LSTM(50, activation="relu", input_shape=(time_steps, X_train.shape[1])))
lstm_model.add(Dense(1))
lstm_model.compile(optimizer="adam", loss="mse")

history = lstm_model.fit(X_train_seq, y_train_seq, epochs=20, batch_size=4, validation_split=0.1)

y_pred_lstm = lstm_model.predict(X_test_seq)


mse_lstm = mean_squared_error(y_test_seq, y_pred_lstm)
r2_lstm = r2_score(y_test_seq, y_pred_lstm)
print("\nLSTM Model Performance:")
print(f"MSE: {mse_lstm:.4f}, R²: {r2_lstm:.4f}")

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred_lr, color="blue", alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
plt.xlabel("Actual Soil Moisture (Norm)")
plt.ylabel("Predicted Soil Moisture (Norm)")
plt.title(f"Linear Regression: R² = {r2_lr:.4f}")

plt.subplot(1, 2, 2)
plt.plot(y_test_seq, label="Actual Soil Moisture", color="green")
plt.plot(y_pred_lstm, label="Predicted Soil Moisture", color="orange", linestyle="--")
plt.xlabel("Time Steps")
plt.ylabel("Soil Moisture (Norm)")
plt.title(f"LSTM: R² = {r2_lstm:.4f}")
plt.legend()

plt.tight_layout()
plt.savefig("model_predictions.png", dpi=300, bbox_inches="tight")
plt.show()

import joblib
joblib.dump(lr_model, "linear_regression_model.pkl")
lstm_model.save("lstm_model.h5")
print("\nModels saved successfully.")
