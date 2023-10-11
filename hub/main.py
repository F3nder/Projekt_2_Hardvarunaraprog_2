import paho.mqtt.client as mqtt
import serial
import json
import time
import struct

# Read configuration from 'config.json' file
with open("hub/config.json") as conf:
    data = json.load(conf) 

# Get configuration values or use default values if not found
name = data.get("name", "Unknown")
broker = data.get("broker", "Unknown")
topic = data.get("topic", "Unknown")

# Initialize an MQTT client and connect to the broker
client = mqtt.Client()
client.connect(broker, port=1883, keepalive=60)
client.loop_start()

# Continuously read data from a serial port and publish it to MQTT
while True:
    # Establish a serial connection to the specified port with a baud rate of 115200
    with serial.Serial('COM5', 115200, timeout=1) as ser:
        line = ser.readline()
        timestamp = time.time()
        timestamp_int = int(timestamp)

        if len(line) > 0:
            line_split = line.split()
            pico_id = line_split[0]
            temp_id = line_split[1]
            temp = line_split[2]
            
            # Decode bytes to UTF-8 strings
            pico_id_decode = pico_id.decode('utf-8')
            temp_id_decode = temp_id.decode('utf-8')
            temp_decode = temp.decode('utf-8')
            
            # Converts temp
            temp_float = float(temp_decode)
            temp_round = int(temp_float * 1000)

             # Pack the timestamp and temperature data into a binary payload
            payload_ = struct.pack('>Ii', timestamp_int, temp_round)

             # Construct the MQTT topic based on configuration and received data
            long_topic = f"{topic}/{name}/{pico_id_decode}/{temp_id_decode}"

            # Publish the payload to the MQTT broker with QoS 1
            msg = client.publish(long_topic, payload=payload_, qos=1)
            msg.wait_for_publish()