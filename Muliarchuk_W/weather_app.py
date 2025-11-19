import os
import platform
from dotenv import load_dotenv
from weather_package import weather_module
from datetime import datetime, timezone, timedelta


def main():
    load_dotenv()
    
    print(f"Операційна система: {platform.system()} {platform.release()}")
    print(f"Версія ядра/системи: {platform.version()}")
    print(f"Python: {platform.python_version()}")
    print()
    
    api_key = weather_module.GetApiKey()
    if api_key.startswith("Error:"):
        print("Помилка: API_KEY не встановлено як змінна середовища")
        print("Отримайте ключ на: https://home.openweathermap.org/")
        return
    
    user_city = input("Введіть назву міста: ").strip()
    if not user_city:
        print("Помилка: назва міста не може бути порожньою")
        return
    
    weather_data = weather_module.GetWeatherData(user_city)
    
    if "error" in weather_data:
        print(f"Помилка виконання запиту: {weather_data['error']}")
        return
    
    result = weather_module.FormatWeatherReport(user_city, weather_data)
    print(result)


if __name__ == "__main__":
    main()
