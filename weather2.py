import argparse
import requests
import sys

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
API_KEY = ""
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# ==========================================
# 📡 API LOGIC
# ==========================================
def get_weather_data(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"❌ Error: City '{city_name}' not found.")
            return None
        else:
            print(f"❌ Error: API returned status code {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

# ==========================================
# 🖥️ DISPLAY LOGIC
# ==========================================
def display_weather(data):
    if not data:
        return
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    desc = data['weather'][0]['description']
    humidity = data['main']['humidity']

    print("-" * 30)
    print(f"🌍 Weather in {city}, {country}")
    print("-" * 30)
    print(f"🌡️  Temperature: {temp}°C")
    print(f"☁️  Condition:   {desc.capitalize()}")
    print(f"💧 Humidity:    {humidity}%")
    print("-" * 30)

# ==========================================
# 🎮 MAIN INPUT LOGIC (UPDATED)
# ==========================================
def main():
    # 1. Setup Argparse to be OPTIONAL
    # We use nargs='?' so the script doesn't crash if you don't type a city at start
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs="?", type=str, help="Name of the city")
    args = parser.parse_args()

    # 2. Define a variable to hold the current city name
    current_city = args.city

    # 3. Start the Loop
    while True:
        # If we don't have a city yet (or we are looping back), ask the user
        if not current_city:
            current_city = input("Enter a city name (or type 'q' to quit): ")

        # Check if user wants to quit
        if current_city.lower() in ['q', 'quit', 'exit', 'no']:
            print("👋 Bye!")
            break

        # 4. Run the weather logic
        print(f"🔍 Searching weather for {current_city}...")
        weather_data = get_weather_data(current_city)
        display_weather(weather_data)

        # 5. Reset current_city to None so the loop asks for a NEW input next time
        current_city = None 

if __name__ == "__main__":

    main()
