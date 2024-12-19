
#!/usr/bin/python
# Copyright (c) 2018-2019 Stijn D'haese

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import Adafruit_DHT
import os
from influxdb import client as influxdb

#Read Data From DHT22 Sensor
humidity, temperature = Adafruit_DHT.read_retry(22, 2)

#InfluxDB Connection Details
influxHost = 'localhost'
influxUser = 'admin'
with open(os.path.dirname(os.path.abspath(__file__)) + '/secretstring', 'r') as f:
    influxPasswd = f.readline().strip()
f.close()

#InfluxDB data
influxdbName = 'temperature'

#return influxDB friendly time 2017-02-26T13:33:49.00279827Z (not really required, but meh)
current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

influx_metric = [{
    'measurement': 'TemperatureSensor',
    'time': current_time,
    'fields': {
        'temperature': temperature,
        'humidity': humidity
    }
}]

#Saving data to InfluxDB
try:
    db = influxdb.InfluxDBClient(influxHost, 8086, influxUser, influxPasswd, influxdbName)
    db.write_points(influx_metric)
finally:
    db.close()