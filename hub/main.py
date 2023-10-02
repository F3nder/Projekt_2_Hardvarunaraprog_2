import paho.mqtt.client as mqtt
import serial
import json

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
        if len(line) > 0:
            line_split = line.split()
            pico_id = bytes(line_split[0])
            temp_id = bytes(line_split[1])
            temp = bytes(line_split[2])
            
            pico_id_decode = pico_id.decode('utf-8')
            temp_id_decode = temp_id.decode('utf-8')

            temp_decode = temp.decode('utf-8')
            temp_decode_float = float(temp_decode)
            temp_decode_float = temp_decode_float * 1000
            
            long_topic = f"{topic}/{name}/{pico_id_decode}/{temp_id_decode}"

            msg = client.publish(long_topic, payload=temp_decode_float, qos=1)
            msg.wait_for_publish()

    # if input() == 0:
    #     client.disconnect()
    #     ser.close()