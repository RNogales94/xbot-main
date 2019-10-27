import os

BOT_KEY = os.environ["BOT_KEY"]

BOT_URL = f'https://api.telegram.org/bot{BOT_KEY}/'  # <-- add your telegram token as environment variable


if __name__ == "__main__":
    print(BOT_KEY)