# 📦 Importing necessary tools
import requests  # To get weather data from the internet
import matplotlib.pyplot as plt  # To create charts and graphs
from datetime import datetime  # To work with dates and times
import numpy as np  # For handling numbers and arrays
import tkinter as tk  # For making popup windows
from tkinter import simpledialog, messagebox  # For input and message popups

# ✅ Making sure emoji can be shown in the chart
plt.rcParams['font.family'] = 'Segoe UI Emoji'

# 🔐 API key to access OpenWeatherMap
api_key = "0a07f78a77320e1c9210d3ce92ce0f39"

# 🧾 Asking the user to enter a city name using a popup window
root = tk.Tk()
root.withdraw()  # Hide the main window
city = simpledialog.askstring("City Input", "Enter city name(e.g. Mumbai, London):")
if not city:
    messagebox.showinfo("Cancelled", "No city entered. Exiting.")
    exit()  # Stop if no city is entered

# 🌐 Creating the link to get weather data for the given city
url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

# 🔄 Trying to get the data from the internet
try:
    response = requests.get(url, timeout=10)
    data = response.json()

    # 🛑 If something goes wrong with the API, show an error message
    if data.get("cod") != "200":
        messagebox.showerror("Error", f"API Error: {data.get('message')}")
        exit()

except requests.exceptions.RequestException as e:
    messagebox.showerror("Connection Error", str(e))
    exit()

# 🕒 Choosing specific times of the day to show in the graph
time_slots = {
    "06:00:00": "Morning",
    "12:00:00": "Afternoon",
    "18:00:00": "Evening",
    "21:00:00": "Night"
}

# 🌦️ Matching weather types to emojis
weather_emojis = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Wind": "🌬️"
}

# 📦 Organizing the weather data by day and time slot
forecast_data = {}

for forecast in data["list"]:
    dt_txt = forecast["dt_txt"]  # Example: "2025-05-24 06:00:00"
    date_part, time_part = dt_txt.split()

    if time_part in time_slots:
        slot = time_slots[time_part]
        date_label = datetime.strptime(date_part, "%Y-%m-%d").strftime("%a %d %b")
        temp = forecast["main"]["temp"]
        weather = forecast["weather"][0]["main"]
        emoji = weather_emojis.get(weather, "")

        if date_label not in forecast_data:
            forecast_data[date_label] = {}

        forecast_data[date_label][slot] = (temp, emoji)

# ✅ FIXED: Sorting dates correctly by appending a dummy year to avoid DeprecationWarning
dates = sorted(forecast_data.keys(), key=lambda d: datetime.strptime(d + " 2025", "%a %d %b %Y"))

# 📊 Preparing to draw the bar chart
slot_labels = list(time_slots.values())
x = np.arange(len(dates))
bar_width = 0.2

# 🎨 Colors for each time of day
slot_colors = {
    "Morning": "lightblue",
    "Afternoon": "orange",
    "Evening": "#FFFF99",
    "Night": "black"
}

plt.figure(figsize=(14, 9))  # Set the size of the chart

# 📈 Drawing a bar for each time slot
for i, slot in enumerate(slot_labels):
    temps = [forecast_data[day].get(slot, (None, ""))[0] for day in dates]
    emojis = [forecast_data[day].get(slot, (None, ""))[1] for day in dates]
    safe_temps = [temp if temp is not None else 0 for temp in temps]

    bars = plt.bar(
        x + i * bar_width,  # Move bars slightly to the side
        safe_temps,
        width=bar_width,
        label=slot,
        color=slot_colors.get(slot, "gray")
    )

    # 📝 Adding emoji on top of each bar
    for j, bar in enumerate(bars):
        if temps[j] is not None:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                emojis[j],
                ha='center',
                va='bottom',
                fontsize=16
            )

# 🎨 Final labels and layout
plt.xticks(x + bar_width * 1.5, dates, rotation=45)
plt.title(f"📅 {city} Weather Forecast – 4 Daily Time Slots")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.legend(title="Time of Day")
plt.grid(axis="y", linestyle="--", alpha=0.5)

# 📌 Showing what each emoji means
legend_lines = [
    "☀️  = Clear",
    "☁️  = Clouds",
    "🌧️ = Rain",
    "🌦️ = Drizzle",
    "⛈️ = Thunderstorm",
    "❄️  = Snow",
    "🌫️ = Mist / Fog",
    "🌬️ = Wind"
]
plt.figtext(1.02, 0.5, "\n".join(legend_lines), fontsize=12, ha="left", va="center", bbox=dict(boxstyle="round", facecolor="#f0f0f0"))

plt.tight_layout()  # Making sure things fit nicely
plt.show()  # 📺 Displaying the chart
