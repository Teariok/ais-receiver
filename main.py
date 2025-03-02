from machine import Pin,UART
import time
from network_manager import NetworkManager
from umqtt.simple import MQTTClient
import config
from binascii import hexlify

device_id = hexlify(machine.unique_id()).decode()
MQTT_TOPIC_STREAM = '/sensor/'+device_id+'/stream'

wifi = NetworkManager(config.wifi_ssid, config.wifi_password, config.wifi_connect_timeout, config.wifi_max_retries)
wifi.connect()

uart = UART(1, baudrate=config.uart_baudrate, tx=Pin(config.uart_tx_pin), rx=Pin(config.uart_rx_pin))
uart.init(bits=config.uart_bits, parity=None, stop=config.uart_stop)

mqtt = MQTTClient(device_id, config.mqtt_server)
mqtt.connect()

try:
    while True:
        if uart.any(): 
            data = uart.read()
            print("AIS Data: ", data.decode('utf-8'))

            if not wifi.is_connected():
                wifi.connect()
                mqtt.connect()
            
            try:
                mqtt.publish(MQTT_TOPIC_STREAM, data)
            except Exception as e:
                print("MQTT Publish Error ", e)
                mqtt.connect(False)

        time.sleep(config.loop_sleep)
except Exception as e:
    print('Error:', e)
