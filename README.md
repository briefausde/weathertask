# weather
Django приложение для получения прогноза погоды по названию города или вашей текущей геолокации.
Для запуска нужно установить все библиотеки из файла requirements.txt, а также перед запуском сделать миграции.

Библиотеки:
- django==1.11.0
- weather-api
- geocoder

Комманды, которые нужно выполнить перед запуском:
- python manage.py makemigrations
- python manage.py migrate
