import requests  # Import the requests library to make HTTP requests
import datetime  # Import the datetime module to work with dates and times
from aiogram import Bot, types  # Import necessary classes from the aiogram library
from aiogram.dispatcher import Dispatcher  # Import the Dispatcher class
from aiogram.utils import executor  # Import the executor utility function


class WeatherBot:
    def __init__(self, telegram_token, open_weather_token):
        """
        Initialize the WeatherBot.

        Args:
            telegram_token (str): Telegram API token.
            open_weather_token (str): OpenWeatherMap API token.
        """
        self.bot = Bot(token=telegram_token)
        self.dp = Dispatcher(self.bot)
        self.user_data = {}

        self.commands = [
            "/start - Get weather information",
            "/suggestions - Get suggestions for things to do",
        ]

        self.code_to_smile = {
            "Clear": "Clear ☀️",
            "Clouds": "Cloudy ☁️",
            "Rain": "Rainy ☔️",
            "Drizzle": "Drizzle ☔️",
            "Thunderstorm": "Thunderstorm ⚡️",
            "Snow": "Snow ❄️",
            "Mist": "Mist 🌫️"
        }

        self.open_weather_token = open_weather_token

        self.dp.message_handler(commands=['start'])(self.start_command)
        self.dp.message_handler(commands=['suggestions'])(self.suggestions_command)
        self.dp.message_handler()(self.get_weather)

    async def start_command(self, message: types.Message):
        """
        Handle the /start command.

        Args:
            message (types.Message): The received message object.
        """
        commands_message = "\n".join(self.commands)
        response_message = f"Hey, which city would you like to know the weather for today?\n\nAvailable commands:\n{commands_message}"
        await message.reply(response_message)

    async def suggestions_command(self, message: types.Message):
        """
        Handle the /suggestions command.

        Args:
            message (types.Message): The received message object.
        """
        user_id = message.from_user.id
        if user_id in self.user_data:
            city = self.user_data[user_id]
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather"
                params = {
                    "q": city,
                    "appid": self.open_weather_token,
                    "units": "metric"
                }
                response = requests.get(url, params=params)
                data = response.json()

                weather_description = data["weather"][0]["main"]

                if weather_description == "Clear":
                    suggestions = "Here are some suggestions for things to do today:\n1. Visit a local park\n2. Have " \
                                  "a picnic\n3. Go for a bike ride\n4. Take a walk on the beach\nEnjoy the sunny day!"
                elif weather_description == "Clouds":
                    suggestions = "Here are some suggestions for things to do today:\n1. Explore a local museum\n2. " \
                                  "Go shopping\n3. Read a book\n4. Watch a movie\nEnjoy the cloudy day!"
                elif weather_description == "Rain" or weather_description == "Drizzle":
                    suggestions = "Here are some suggestions for things to do today:\n1. Visit a cozy cafe\n2. Try a " \
                                  "new recipe at home\n3. Have a movie marathon\n4. Do some indoor exercises\nEnjoy " \
                                  "the rainy day!"
                elif weather_description == "Thunderstorm":
                    suggestions = "Here are some suggestions for things to do today:\n1. Stay indoors and watch a " \
                                  "movie\n2. Read a book\n3. Listen to music\n4. Do some indoor activities\nStay safe " \
                                  "during the thunderstorm!"
                elif weather_description == "Snow":
                    suggestions = "Here are some suggestions for things to do today:\n1. Build a snowman\n2. Have a " \
                                  "snowball fight\n3. Go skiing or snowboarding\n4. Enjoy a cup of hot " \
                                  "chocolate\nHave fun in the snow!"
                elif weather_description == "Mist":
                    suggestions = "Here are some suggestions for things to do today:\n1. Go for a scenic drive\n2. " \
                                  "Visit a local art gallery\n3. Have a warm drink at a cozy cafe\n4. Explore a " \
                                  "botanical garden\nEnjoy the misty day!"

                await message.reply(suggestions)

            except Exception:
                await message.reply(
                    "Oops! Something went wrong while getting weather information.")

        else:
            await message.reply(
                "Please use the /start command first to provide a city name.")

    async def get_weather(self, message: types.Message):
        """
        Get the weather information for the specified city.

        Args:
            message (types.Message): The received message object.
        """
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": message.text,
                "appid": self.open_weather_token,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            data = response.json()

            city = data["name"]
            user_id = message.from_user.id
            self.user_data[user_id] = city

            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            wd = self.code_to_smile.get(weather_description,
                                        "Look out the window, I can't understand the weather there!")

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = sunset_timestamp - sunrise_timestamp

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            weather_message = (
                f"***{current_time}***\n"
                f"Weather in {city}:\n"
                f"Temperature: {cur_weather}°C {wd}\n"
                f"Humidity: {humidity}%\n"
                f"Pressure: {pressure} mmHg\n"
                f"Wind: {wind} m/s\n"
                f"Sunrise: {sunrise_timestamp}\n"
                f"Sunset: {sunset_timestamp}\n"
                f"Length of the day: {length_of_the_day}\n"
                f"***Have a nice day!***\n\n"
                f"Would you like me to suggest things to do today? Use the /suggestions command."
            )

            await message.reply(weather_message)

        except Exception:
            await message.reply("\U00002620 Check the city name \U00002620")

    def run(self):
        """
        Start the WeatherBot.
        """
        print("WeatherBot is running now.")
        executor.start_polling(self.dp)



