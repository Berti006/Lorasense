import socket
import binascii
import struct
import time
import pycom
import network
from network import LoRa
from network import WLAN

mac = binascii.hexlify(network.LoRa().mac())


print("*************************************")
print("     LoraSense 0.1")
print("")
print("WiFi MAC: ")
print("LORA MAC: " + mac.upper().decode('utf-8'))
print("*************************************")

pycom.heartbeat(False)
pycom.rgbled(0x000000)
# Initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('00000001'))[0]
nwk_swkey = binascii.unhexlify('2B7E151628AED2A6ABF7158809CF4F3C')
app_swkey = binascii.unhexlify('2B7E151628AED2A6ABF7158809CF4F3C')

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

while True:
    print("Sending JSON data")
    pycom.rgbled(0xff0000)
    # send some data
    s.setblocking(True)
    s.send('{ "node" : "Lorasense", "nodeID" : "0001"}')
    pycom.rgbled(0xff00ff)
    s.setblocking(False)
    data = s.recv(64)
    print(data)
    pycom.rgbled(0x000000)
    time.sleep(60)
# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)
