#main.py
import machine, onewire, ds18x20, time
import ujson

with open("config.json") as conf:
    data = ujson.load(conf) 
    
pin = data.get("pin", "Unknown")
interval = data.get("interval", "Unknown")
# print(pin)      #debug
# print(interval) #debug


ds_pin = machine.Pin(pin)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

if not roms:
    raise RuntimeError("Found no DS18b20")
    
while True:
  ds_sensor.convert_temp()
  time.sleep_ms(interval*10)
  for rom in roms:
    print(ds_sensor.read_temp(rom))
  time.sleep(1)