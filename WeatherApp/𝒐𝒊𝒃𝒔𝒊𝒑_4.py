import tkinter as tk
import requests
from PIL import Image, ImageTk
import io

def get_weather():
    city = city_entry.get()
    api_key = "98394a7248ac629e8xxxxxxxxx"  # Replace "YOUR_API_KEY" with your actual API key

    # API call to fetch weather data
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors (4xx or 5xx)
        weather_data = response.json()

        # Extract relevant weather information
        if weather_data["cod"] == 200:
            temperature = weather_data["main"]["temp"]
            weather_desc = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]

            # Display weather information
            result_label.config(text=f"Temperature: {temperature} °C\n"
                                      f"Weather: {weather_desc}\n"
                                      f"Humidity: {humidity}%\n"
                                      f"Wind Speed: {wind_speed} m/s")

            # Display weather icon
            icon_code = weather_data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_data = requests.get(icon_url).content
            icon_image = ImageTk.PhotoImage(Image.open(io.BytesIO(icon_data)))
            weather_icon_label.config(image=icon_image)
            weather_icon_label.image = icon_image  # Keep a reference to prevent garbage collection

        else:
            result_label.config(text="City not found")
    except requests.exceptions.HTTPError:
        result_label.config(text="Error fetching data. Please try again later.")

# GUI setup
root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter City:")
city_label.grid(row=0, column=0, padx=10, pady=5)

city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=5)

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.grid(row=1, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

weather_icon_label = tk.Label(root)
weather_icon_label.grid(row=2, column=2, padx=10, pady=5)  # Place the weather icon to the right of the weather information
root.bind("<Return>", get_weather_button)
root.mainloop()
