import network
import usocket as socket
from machine import Pin, I2C
import bme280


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Wi-Fi connected:', wlan.ifconfig())


i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
bme = bme280.BME280(i2c=i2c)


wifi_ssid = "The Iqbal's"
wifi_password = "Zeeshan786"
connect_wifi(wifi_ssid, wifi_password)


html = """<!DOCTYPE html>
<html>
<head><title>BME280 Sensor Readings</title></head>
<body>
<h1>BME280 Sensor Readings</h1>
<p>Temperature: {:.2f} °C</p>
<p>Humidity: {:.2f} %</p>
<p>Pressure: {:.2f} hPa</p>
</body>
</html>
"""


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 80))  
server_socket.listen(5)  

while True:
    print('Waiting for connection...')
    client_socket, client_address = server_socket.accept()
    print('Client connected from:', client_address)

    
    request = client_socket.recv(1024)

    
    temperature, pressure, humidity = bme.read_compensated_data()
    response = html.format(temperature / 100, humidity / 1024, pressure / 25600)
    client_socket.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}".format(len(response), response))

    
    client_socket.close()
