import os
import requests
from typing import Optional
from datetime import datetime, timezone, timedelta


def GetApiKey() -> str:
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: key not found"
        return api_key
    except Exception as e:
        return f"Error: {str(e)}"


def GetWeatherData(city: str, units: str = "metric") -> dict:
    try:
        api_key = GetApiKey()
        if api_key.startswith("Error:"):
            return {"error": api_key}
        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": units, "lang": "ua"}
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            return {"error": f"API error: {response.status_code}"}
        
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def FormatWeather(weather_data: dict, units: str = "metric") -> str:
    try:
        if "error" in weather_data:
            return weather_data["error"]
        
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "м/с" if units == "metric" else "mph"
        
        city = weather_data.get("name", "Unknown")
        country = weather_data.get("sys", {}).get("country", "")
        
        main = weather_data.get("main", {})
        temp = main.get("temp", 0)
        feels = main.get("feels_like", 0)
        temp_min = main.get("temp_min", 0)
        temp_max = main.get("temp_max", 0)
        pressure = main.get("pressure", 0)
        humidity = main.get("humidity", 0)
        
        desc = weather_data.get("weather", [{}])[0].get("description", "Unknown")
        
        wind = weather_data.get("wind", {})
        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", 0)
        
        clouds = weather_data.get("clouds", {}).get("all", 0)
        visibility = weather_data.get("visibility", 0)
        
        result = f"{city}, {country}\n"
        result += f"Description: {desc}\n\n"
        result += f"Temperature: {temp:.1f}{temp_unit} (feels {feels:.1f}{temp_unit})\n"
        result += f"Min/Max: {temp_min:.1f}/{temp_max:.1f}{temp_unit}\n"
        result += f"Pressure: {pressure} hPa | Humidity: {humidity}%\n"
        result += f"Wind: {wind_speed:.1f} {speed_unit}, {wind_deg}°\n"
        result += f"Clouds: {clouds}% | Visibility: {visibility/1000:.1f} km"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def GetWeatherSimple(city: str) -> str:
    try:
        data = GetWeatherData(city)
        if "error" in data:
            return data["error"]
        return FormatWeather(data)
    except Exception as e:
        return f"Error: {str(e)}"


def GetWindDirection(degrees: int) -> str:
    try:
        dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        idx = round(degrees / 45) % 8
        return dirs[idx]
    except Exception as e:
        return f"Error: {str(e)}"


def ConvertTemperature(celsius: float, to_unit: str = "fahrenheit") -> str:
    try:
        if to_unit.lower() == "fahrenheit":
            f = (celsius * 9/5) + 32
            return f"{f:.1f}°F"
        elif to_unit.lower() == "kelvin":
            k = celsius + 273.15
            return f"{k:.1f}K"
        else:
            return f"{celsius:.1f}°C"
    except Exception as e:
        return f"Error: {str(e)}"


def FormatWeatherReport(user_city: str, weather_data: dict) -> str:
    try:
        if "error" in weather_data:
            return weather_data["error"]
        
        api_city = weather_data.get("name", "Unknown")
        
        tz_offset_sec = weather_data.get("timezone", 0)
        tz_hours = tz_offset_sec // 3600
        tz_mins = abs(tz_offset_sec % 3600) // 60
        tz_sign = "+" if tz_offset_sec >= 0 else "-"
        timezone_str = f"UTC{tz_sign}{abs(tz_hours):02d}:{tz_mins:02d}"
        
        ukraine_tz = timezone(timedelta(hours=3))
        local_time = datetime.now(ukraine_tz).strftime("%Y-%m-%d %H:%M:%S%z")
        local_time_formatted = local_time[:-2] + ":" + local_time[-2:]
        
        sunrise = weather_data.get("sys", {}).get("sunrise", 0)
        sunset = weather_data.get("sys", {}).get("sunset", 0)
        day_length_sec = sunset - sunrise
        day_hours = day_length_sec // 3600
        day_mins = (day_length_sec % 3600) // 60
        
        main = weather_data.get("main", {})
        temp = main.get("temp", 0)
        feels_like = main.get("feels_like", 0)
        humidity = main.get("humidity", 0)
        
        desc = weather_data.get("weather", [{}])[0].get("description", "немає даних")
        
        wind_speed = weather_data.get("wind", {}).get("speed", 0)
        
        result = f"Погода у місті {user_city} ({api_city}):\n"
        result += f"Часова зона: {timezone_str}\n"
        result += f"Дата і час запиту (локальний час): {local_time_formatted}\n"
        result += f"Тривалість дня: {day_hours}:{day_mins:02d} (г:хв)\n"
        result += f"Опис: {desc}\n"
        result += f"Температура: {temp:.2f}°C (відчувається як {feels_like:.2f}°C)\n"
        result += f"Вологість: {humidity}%\n"
        result += f"Швидкість вітру: {wind_speed:.2f} м/с"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"
