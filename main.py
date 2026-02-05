import network
import time
from machine import Pin, I2C
import bme280
from umqttsimple import MQTTClient
import myconfig

# 1. Setup WiFi (Required for MQTT)
WIFI_SSID = myconfig.WIFI_SSID
WIFI_PASS = myconfig.WIFI_PASS

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        time.sleep(1)
print("WiFi Connected:", wlan.ifconfig())

# 2. Initialize BME280 with correct address
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
try:
    # Explicitly setting address to 0x76
    b = bme280.BME280(i2c=i2c, address=0x76)
except Exception as e:
    print("Could not initialize BME280:", e)
    raise SystemExit

# 3. Setup MQTT

TOPIC = "gcdemo/esp32/bme280"

mqtt = MQTTClient(
    client_id=myconfig.CLIENT_ID,
    server=myconfig.BROKER,
    port=myconfig.PORT,
    user=myconfig.USER_NAME,
    password=myconfig.PASSWORD,
    ssl=True,
    ssl_params={"server_hostname": myconfig.BROKER} 
)
mqtt.connect()

while True:
    try:
        # Note: Check your specific bme280 library documentation. 
        # Some use .values, some use .read_compensated_data()
        readings = b.values 
        payload = "{} {} {}".format(readings[0], readings[1], readings[2])
        
        mqtt.publish(TOPIC, payload)
        print("Sent:", payload)
    except Exception as e:
        print("Loop error:", e)
        
    time.sleep(5)
