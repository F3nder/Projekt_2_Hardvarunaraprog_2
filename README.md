# Projekt_2_Hardvarunaraprog_2

BOM-list
Raspberry pi pico H
DS18B20 - (temp sensor)
Kopplingskablar (male to male)
USB - datakabel 

sensor/config.json
Inställningar för vilken GPIO pin som används för sensorn och mät intervall

hub/config.json
Inställningar för namn brooker och topic (vart datan skall skickas)



Step by step
1. Koppla upp sensorn till 3,3V, GND och GPIO16

2. Kopiera över main.py och config.json från sensor-mappen till Raspberryn medhjälp av "mpremote cp main.py :"
   och "mpremote cp config.json :"

3. Reseta Raspberryn "mpremote reset"

5. Kontrollera vilken COM-port som Raspberryn är ansluten till via enhetshanteraren och skriv in rätt COM-port på rad 22
   i hub/main.py

4. Starta hub/main.py 



OBS!!!
temp2.py bara för debugging på Raspberryn 