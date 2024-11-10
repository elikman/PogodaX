#  Проект Погода

## О проекте

Телеграмм бот, который скидывает погоды.

## Стек

<img src="https://img.shields.io/badge/Python-FFFFFF?style=for-the-badge&logo=python&logoColor=3776AB"/>><img src="https://img.shields.io/badge/Docker-FFFFFF?style=for-the-badge&logo=Docker&logoColor=2496ED"/><img src="https://img.shields.io/badge/Yandex Cloud-FFFFFF?style=for-the-badge&logo=Yandex Cloud&logoColor=5282FF"/>

### Как запустить проект через Docker:
1. Клонируйте репозиторий проекта
2. Cоздать и активировать виртуальное окружение:
Windows
```
python -m venv venv
source venv/Scripts/activate
```
Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```
3. Обновить PIP
Windows
```
python -m pip install --upgrade pip
```
Linux/macOS
```
python3 -m pip install --upgrade pip
```
4. Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
5. Заполните ```.env``` файл:
```
BOT_TOKEN = "сюда ключ надо вставить"
WEATHER_API_KEY = "сюда ключ надо вставить"
```
6. Запустить через Docker:
```
docker compose up
```
7. Запустить через локально:
```
python weather_bot.py
```

#### Ссылка на телеграмм бота
```https://t.me/GoodRainyAzBot```