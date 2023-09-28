import paho.mqtt.client as mqtt
import serial

# Create a MQTT client and register a callback for connect events
client = mqtt.Client()

# Connect to a broker
client.connect("broker.hivemq.com", port=1883, keepalive=60)

# Start a background loop that handles all broker communication
client.loop_start()

pico_id = 0
temp_id = 0
temp = 0
while True:
    with serial.Serial('COM5', 115200, timeout=1) as ser:
        line = ser.readline()
        if len(line) > 0:
            # line_decode = line.decode('utf-8')
            line_split = line.split()
            print(line_split)
            pico_id = bytes(line_split[0])
            temp_id = bytes(line_split[1])
            temp = bytes(line_split[2])

            for byte in pico_id:
                print(byte, end=" ")
            print("\n")

            for byte2 in temp_id:
                print(byte2, end=" ")
            print("\n")

            for byte3 in temp:
                print(byte3, end=" ")
            print("\n")

    
# Send the message
    msg = client.publish("yrgo/ela/chat2", payload=temp, qos=1)
    if len(temp) == 0:
        break
# If python exits immediately it does not have the time to send
# the message
    msg.wait_for_publish()

client.disconnect()
ser.close()