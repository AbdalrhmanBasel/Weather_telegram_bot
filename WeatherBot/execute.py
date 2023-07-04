import os

from dotenv import load_dotenv

from WeatherBot import WeatherBot

if __name__ == '__main__':
    load_dotenv()
    weather_bot = WeatherBot(os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("OPEN_WEATHER_TOKEN"))
    weather_bot.run()
