#main.py
import machine, onewire, ds18x20, time, ujson

# Read the configuration from the "config.json" file
with open("config.json") as conf:
    data = ujson.load(conf) 
    
# Get the 'pin' and 'interval' values from the configuration, or use default values if not found
pin = data.get("pin", "Unknown")
interval = data.get("interval", "Unknown")

# Function to get the unique ID of the Pico board and convert it to a hexadecimal string
def pico_id_get():
  pico_id = machine.unique_id()
  pico_id_hex = pico_id.hex()
  return pico_id_hex

# Function to convert the ROM (unique identifier) of a DS18b20 temperature sensor to a hexadecimal string
def temp_id_get(rom):
   temp_id = rom
   temp_id_hex = temp_id.hex()
   return temp_id_hex

# Initialize the OneWire bus and DS18X20 sensor using the specified pin
ds_pin = machine.Pin(pin)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# Scan for DS18b20 temperature sensors on the OneWire bus
roms = ds_sensor.scan()

# Raise an error if no DS18b20 sensors are found
if not roms:
    raise RuntimeError("Found no DS18b20")
    
# Main loop: continuously read temperature data from the DS18b20 sensors
while True:
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  for rom in roms:
    print(pico_id_get(), temp_id_get(rom), ds_sensor.read_temp(rom))
  time.sleep(interval)