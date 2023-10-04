import paho.mqtt.client as mqtt
import serial
import json
import time
import struct

with open("hub/config.json") as conf:
    data = json.load(conf) 
name = data.get("name", "Unknown")
broker = data.get("broker", "Unknown")
topic = data.get("topic", "Unknown")



client = mqtt.Client()
client.connect(broker, port=1883, keepalive=60)
client.loop_start()

while True:
    with serial.Serial('COM5', 115200, timeout=1) as ser:
        line = ser.readline()
        timestamp = time.time()
        timestamp_int = int(timestamp)
        if len(line) > 0:
            line_split = line.split()
            pico_id = line_split[0]
            temp_id = line_split[1]
            temp = line_split[2]
            
            pico_id_decode = pico_id.decode('utf-8')
            temp_id_decode = temp_id.decode('utf-8')

            temp_decode = temp.decode('utf-8')
            temp_float = float(temp_decode)
            temp_round = int(temp_float * 1000)

            payload_ = struct.pack('>Ii', timestamp_int, temp_round)
            long_topic = f"{topic}/{name}/{pico_id_decode}/{temp_id_decode}"

            msg = client.publish(long_topic, payload=payload_, qos=1)
            msg.wait_for_publish()