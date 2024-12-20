#!/usr/bin/python3
# Copyright (c) 2018-2019 Stijn D'haese
# Licensed under the MIT License

from datetime import datetime, timezone
import Adafruit_DHT
import os
from influxdb import InfluxDBClient  # Biblioteca para InfluxDB 1.x
from telegram import Bot
 
HOST = 'localhost'
PORT = 8086
USER = 'admin'
DB_NAME = 'temperature'
TELEGRAM_TOKEN = '1321102558:AAHOEaSXY7uWU14Q5C8A_sZZM--0km2KNsw'
CHAT_ID = '-881981569'
current_time = datetime.now(timezone.utc).isoformat()


def send_telegram_alert(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"Erro ao enviar alerta para o Telegram: {e}")

def getHumidityAndTemperature():
    humidity, temperature = Adafruit_DHT.read_retry(22, 2)

    if humidity is None or temperature is None:
        send_telegram_alert("Erro ao ler os dados do sensor. Verifique a conexão.")
        exit(1)

    return humidity, temperature

def getPasswd():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/secretstring', 'r') as f:
        return f.readline().strip()

def feedInfluxMetric(humidity, temperature):
    influx_metric = [
        {
            'measurement': 'TemperatureSensor',
            'time': current_time,
            'fields': {
                'temperature': temperature,
                'humidity': humidity
            }
        }
    ]
    return influx_metric



def main():
    send_telegram_alert('Rasp Started successfully :)')
    humidity, temperature = getHumidityAndTemperature()
    influx_metric = feedInfluxMetric(humidity, temperature)

    try:
        db_client = InfluxDBClient(
            host=HOST,
            port=PORT,
            username=USER,
            password=getPasswd(),
            database=DB_NAME
        )

        db_client.write_points(influx_metric)

        print(f"Dados enviados com sucesso: {influx_metric}")

    except Exception as e:
        send_telegram_alert(f"Erro ao enviar dados para o InfluxDB: {e}")
    finally:
        db_client.close()


main()


