from dotenv import load_dotenv
import os

load_dotenv(override=True)

BOT_KEY = os.getenv('BOT_KEY')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASS = os.getenv('RABBIT_PASS')
RABBIT_HOST = os.getenv('RABBIT_HOST')

print(BOT_KEY)
print(RABBIT_USER)
print(RABBIT_PASS)
print(RABBIT_HOST)