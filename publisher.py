import network
import time
from machine import Pin, I2C
import bme280
from umqttsimple import MQTTClient

# 1. Setup WiFi (Required for MQTT)
WIFI_SSID = "ganny17"
WIFI_PASS = "ganeshc#"

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

CLIENT_ID = "esp32-bme280-demo"
TOPIC = "gcdemo/esp32/bme280"
BROKER="5c97a09b9c584c019524294c3a521b42.s1.eu.hivemq.cloud"
PORT=8883
USER_NAME="gcadmin1"
PASSWORD="Qi6dFTp@e8jeYCn"

mqtt = MQTTClient(
    client_id=CLIENT_ID,
    server=BROKER,
    port=PORT,
    user=USER_NAME,
    password=PASSWORD,
    ssl=True,
    ssl_params={"server_hostname": BROKER} 
)
#mqtt = MQTTClient(CLIENT_ID, BROKER)
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
        
    time.sleep(2)
