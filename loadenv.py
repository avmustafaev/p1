import os
from pathlib import Path

from dotenv import load_dotenv

""" Модуль подтягивает параметры настроек из файла .env
и загружает в переменные окружения, затем из переменных окружения
инициализирует настройки в переменные модуля
"""

class Envi:
    def __init__(self) -> None:
        env_path = Path(".") / ".env"
        load_dotenv(dotenv_path=env_path)
        self.token = os.getenv("TOKEN")
        print(self.token)

envi = Envi()