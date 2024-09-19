from machine import Pin, I2C
import bme280


i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)


bme = bme280.BME280(i2c=i2c)


temperature, pressure, humidity = bme.read_compensated_data()


temperature /= 100  
humidity /= 1024  
pressure /= 25600  

print("Temperature: {:.2f} °C".format(temperature))
print("Humidity: {:.2f} %".format(humidity))
print("Pressure: {:.2f} hPa".format(pressure))


