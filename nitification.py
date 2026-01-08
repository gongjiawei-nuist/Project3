import smtplib
from email.message import EmailMessage
import pandas as pd
from datetime import datetime


FROM_EMAIL = "bno03972367@163.com"
APP_PASSWORD = "KQxxUSru9RVFkzZC"
TO_EMAIL = "bno03972364@163.com"
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 587
def send_email_with_results():
    """Send sensor data summary and model performance via email"""

    try:
        df = pd.read_csv("preprocessed_data.csv")
        latest_data = df.iloc[-1]y
        timestamp = latest_data["Timestamp"]
        soil_moisture = round(latest_data["Soil_Moisture_Denoised"], 2)
        temperature = round(latest_data["Temperature_Denoised"], 2)
        air_humidity = round(latest_data["Air_Humidity_Denoised"], 2)
        data_summary = (
            f"Latest Sensor Data (Timestamp: {timestamp})\n"
            f"- Soil Moisture (Denoised): {soil_moisture} (0-1023 scale)\n"
            f"- Temperature (Denoised): {temperature} °C\n"
            f"- Air Humidity (Denoised): {air_humidity} %\n"
        )
    except Exception as e:
        data_summary = f"Failed to read sensor data: {str(e)}\n"


    try:
        with open("model_performance.txt", "r") as f:
            model_perf = f.read()
        model_summary = f"Model Prediction Performance:\n{model_perf}\n"
    except Exception as e:
        model_summary = f"Failed to read model performance: {str(e)}\n"

    email_subject = f"Raspberry Pi Sensor & Model Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    email_body = (
        "Raspberry Pi Soil Moisture Prediction Project Report\n"
        "="*50 + "\n\n"
        f"{data_summary}\n"
        f"{model_summary}\n"
        "Note: This email is automatically sent after model training is completed.\n"
    )

    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = email_subject
    msg.set_content(email_body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print(f" Email sent successfully to {TO_EMAIL}")
    except Exception as e:
        print(f" Failed to send email: {str(e)}")
