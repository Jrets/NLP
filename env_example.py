import os

from dotenv import load_dotenv

# относительный путь, рекомендуется глобальный
load_dotenv("./.env")

key = "USERNAME1"
username = os.getenv(key, None)
username1 = os.environ.get(key, None)

print(username)
print(username1)
