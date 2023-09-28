#main.py
import machine, onewire, ds18x20, time, ujson

with open("config.json") as conf:
    data = ujson.load(conf) 
    
pin = data.get("pin", "Unknown")
interval = data.get("interval", "Unknown")

def pico_id_get():
  pico_id = machine.unique_id()
  pico_id_hex = pico_id.hex()
  return pico_id_hex

def temp_id_get(rom):
   temp_id = rom
   temp_id_hex = temp_id.hex()
   return temp_id_hex

ds_pin = machine.Pin(pin)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

if not roms:
    raise RuntimeError("Found no DS18b20")
    
while True:
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    print(pico_id_get(), temp_id_get(rom), ds_sensor.read_temp(rom))
  time.sleep(interval)

# import machine, onewire, ds18x20, time
 
# ds_pin = machine.Pin(16)
# ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# roms = ds_sensor.scan()

# if not roms:
#     raise RuntimeError("Found no DS18b20")
    
# while True:
#   ds_sensor.convert_temp()
#   time.sleep_ms(750)
#   for rom in roms:
#     print(ds_sensor.read_temp(rom))
#   time.sleep(1)