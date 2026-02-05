# ESP32 WROOM (Generic) + BME280 + MQTT over MicroPython

- [ESP32 WROOM (Generic ESP32)](https://www.amazon.com/dp/B0FBV7QGC4)
- [BME280 breakout module (I2C)](https://www.amazon.com/dp/B0DHPCFXCK)
- [Breadboard](https://www.amazon.com/dp/B0CXF1B6GB)
- [Jumper wires](https://www.amazon.com/dp/B01EV70C78)
- USB data cable (not charge-only)
- A Mac, Linux, or Windows machine with Python 3.10+
- WiFi SSID and password
- MQTT broker credentials (example below uses HiveMQ Cloud TLS on 8883)

## Local Python setup

Note: Don't use Dev Container via Docker.

**Option A - Using UV**

```
python3 -m pip install -U uv
uv venv
source .venv/bin/activate
uv pip install esptool mpremote
```

**Option B - Using PIP**

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install esptool mpremote
```

## Wire the BME280 to the ESP32 (I2C)

Most BME280 breakouts expose: VIN (or VCC), GND, SCL, SDA.

Default ESP32 I2C pins (common convention)

- BME280 VIN/VCC → ESP32 3V3
- BME280 GND → ESP32 GND
- BME280 SCL → ESP32 GPIO22
- BME280 SDA → ESP32 GPIO21

## Identify the serial port (ESP32 plugged in)

**macOS**

```
ls /dev/cu.*
```

You’ll typically see something like:

/dev/cu.usbserial-0001
/dev/cu.SLAB_USBtoUART
/dev/cu.wchusbserial*

**Linux**

```
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
```

**Windows**

PowerShell:

```
Get-CimInstance Win32_SerialPort | Select-Object DeviceID,Description
```

**Example Output**

```
macOS example: /dev/cu.usbserial-0001
Linux example: /dev/ttyUSB0
Windows example: COM3
```

**Note: Based on whatever PORT value you see you have to use that port value in following commands**

## Erase the ESP32 flash (clean reset)

This wipes whatever is currently on the board.

**MAC**

Before copying this command remember to check YOUR COMPUTER PORT from above step.

```
esptool --chip esp32 --port /dev/cu.usbserial-0001 erase_flash
```

**Windows**

```
esptool.py --chip esp32 --port COM3 erase_flash
```

## Download the latest MicroPython firmware (.bin)

Go here and download the latest ESP32_GENERIC firmware to the same Virtual Env

https://micropython.org/download/ESP32_GENERIC/

What is the .bin file?

It’s the firmware image that gets written to the ESP32’s flash memory. After flashing it, your ESP32 boots straight into MicroPython.

## Flash MicroPython to the ESP32

From the folder where you downloaded the firmware (example filename below), run:

**Mac**

```
esptool --chip esp32 --port /dev/cu.usbserial-0001 write_flash -z 0x1000 ESP32_GENERIC-*.bin
```

**Windows**

```
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 ESP32_GENERIC-*.bin
```

## Open a MicroPython REPL using mpremote

**Mac**

```
python3 -m mpremote connect /dev/cu.usbserial-0001 repl
```

**Windows**

```
python3 -m mpremote connect COM3 repl
```

Press Enter and you should see the MicroPython prompt:

>>>

If you don’t get >>>, you’re not connected. Fix your port, cable, or permissions.


## Quick sanity checks in the REPL

```
import os, machine
os.uname()
machine.freq()
machine.unique_id()
```
Press Ctrl+X to exit the Python REPL

## Install the BME280 driver on the ESP32 filesystem

Repo: https://github.com/robert-hh/BME280

- Download bme280_float.py
- Rename it to bme280.py
- Copy to the ESP32

**Mac**

```
python3 -m mpremote connect /dev/cu.usbserial-0001 fs cp bme280.py :
```
**Windows**

```
python3 -m mpremote connect COM3 fs cp bme280.py :
```

## Install umqtt.simple

Source: https://raw.githubusercontent.com/micropython/micropython-lib/master/micropython/umqtt.simple/umqtt/simple.py

- Download simple.py
- Rename it to umqttsimple.py
- Copy to the ESP32

**Mac**

```
python3 -m mpremote connect /dev/cu.usbserial-0001 fs cp umqttsimple.py :

```
**Windows**

```
python3 -m mpremote connect COM3 fs cp umqttsimple.py :
```

## Get your app files (main.py + config)

https://github.com/gchandra10/esp32-demo/blob/main/myconfig.template
https://github.com/gchandra10/esp32-demo/blob/main/main.py

- Download them locally
- Download both files into your working folder.
- Rename myconfig.template → myconfig.py
- Edit myconfig.py and set values:

```
WIFI_SSID = ""
WIFI_PASS = ""

CLIENT_ID = ""

BROKER = ".s1.eu.hivemq.cloud"
PORT = 8883

USER_NAME = ""
PASSWORD = ""
```

## Test run from your laptop (without copying yet)

Run your script directly on the board from local disk:

```
python3 -m mpremote connect /dev/cu.usbserial-0001 run main.py
```
**Note:**

- WiFi issues: SSID/password, 2.4GHz vs 5GHz mismatch (ESP32 is usually 2.4GHz)
If you are using personal hotspot, they are usually 5GHz enabled 2.4GHz by enabling Maximize Compatibility

If everything works good then 

## Copy files onto the ESP32 (for standalone boot)

**Mac**

```
python3 -m mpremote connect /dev/cu.usbserial-0001 fs cp myconfig.py :
python3 -m mpremote connect /dev/cu.usbserial-0001 fs cp main.py :
```

**Windows**

```
python3 -m mpremote connect COM3 fs cp myconfig.py :
python3 -m mpremote connect COM3 fs cp main.py :
```

## Power it from a power bank

- Unplug USB from laptop
- Plug into a power bank
- The ESP32 should boot and run main.py automatically

Your device should publish temperature and humidity every 5 seconds (based on your main.py loop)

