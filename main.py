# подключаем модуль для Телеграма
import telebot
import requests

# подключаем токен бота
bot = telebot.TeleBot('6691252717:AAHpMuCC337fl_4U4ucKz_jJlwk8r8b2AIs')

start_txt = (f'Привет!'
'\n\nОтправь название города или населённого пункта, чтобы узнать прогрноз погоды.')


# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

# обрабатываем любой текстовый запрос
@bot.message_handler(content_types=['text'])
def weather(message):
    # получаем город из сообщения пользователя
  if any(char.isdigit() for char in message.text):
      bot.send_message(message.from_user.id, 'Ввод содержит цифры. \n\nОтправь название или населённый пункт, чтобы я прислал прогноз.')


  city = message.text

  # формируем запрос
  url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

  # отправляем запрос на сервер и сразу получаем результат
  response = requests.get(url)
  if response.status_code != 200:
    bot.send_message(message.from_user.id, 'Не могу найти. \n\nНет в базе данных или это выдумка.')

  weather_data = response.json()
  # получаем данные о температуре и о том, как она ощущается

  humidity = (weather_data['main']['humidity'])
  wind_speed = (weather_data['wind']['speed'])
  temperature_feels = round((weather_data['main']['feels_like']), 1)

  temperature = round((weather_data['main']['temp']), 1)
  if -100.0 <= temperature <= -30.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n❄❄❄❄\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')
  elif -30.0 <= temperature <= -20.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n❄❄❄\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')
  elif 0.0 <= temperature <= -10.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n❄❄\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')
  elif 10.0 >= temperature >= 0.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n🌡\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')
  elif 20.0 >= temperature >= 10.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n🌤\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')
  elif 30.0 >= temperature >= 20.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n☀🌤\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')
  elif 100.0 >= temperature >= 30.0:
      bot.send_message(message.from_user.id, 'Сейчас в ' + city + ' ' + str(temperature) + ' °C\n☀☀☀\nОщущается как ' + str(temperature_feels) + ' °C\nВлажность воздуха ' + str(humidity) + ' %\nСкорость верта ' + str(wind_speed) + ' м/с')

# запускаем бота
if __name__ == '__main__':
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые сообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e: 
            print(e)