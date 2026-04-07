import os

import dotenv
import requests
import rich.console as rich_console
import rich.table as rich_table

console = rich_console.Console()

dotenv.load_dotenv()


# Add converter functions to learn unittesting
def convert_fahrenheit_to_celsius(fahrenheit):
    celsius = (5 * fahrenheit - 160) / 9

    return celsius


def convert_celsius_to_fahrenheit(celsius):
    fahrenheit = (celsius * 9 / 5) + 32

    return fahrenheit


def get_weather_data(city: str):
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

    request_parameters = {
        "q": city,
        "appid": os.getenv("OPEN_WEATHER_API_KEY"),
        "units": "metric",
    }

    response = requests.get(WEATHER_API_URL, params=request_parameters)

    if response.status_code not in range(200, 300):
        raise RuntimeError(f"Request failed with status code {response.status_code}")

    data = response.json()

    return data


def display_weather_data(data):
    main = data["main"]
    weather_desc = data["weather"][0]["description"].title()
    city_name = data["name"]
    country = data["sys"]["country"]

    table = rich_table.Table(
        title=f"Weather in {city_name}, {country}",
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    table.add_row("Condition", weather_desc)
    table.add_row("Temperature", f"{main['temp']} °C")
    table.add_row("Feels Like", f"{main['feels_like']} °C")
    table.add_row("Min / Max", f"{main['temp_min']} °C / {main['temp_max']} °C")
    table.add_row("Humidity", f"{main['humidity']}%")

    console.print(table)


def main():
    try:
        print("=" * 80)
        print("Weather App")
        print("=" * 80)

        city = input("City: ")
        print("=" * 80)

        city = city.strip().title()

        data = get_weather_data(city)

        display_weather_data(data)
    except Exception as e:
        print("Some Exception Occured. Try running the program again later.")
        print(e)
    finally:
        print("=" * 80)
        print("Byeeee!!!")
        print("=" * 80)


if __name__ == "__main__":
    main()
