# import pycom
# from network import LoRa
# import socket
# import machine
# import time

# lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# s.setblocking(True)
# s.send('{ "node" : "LoraSense"}')
# s.setblocking(False)
# data.s.recv(64)
# print(data)
from network import LoRa
import socket
import time
import binascii

# Initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters
app_eui = binascii.unhexlify('ADA4DAE3AC12676B') #70B3D54995B808A6
app_key = binascii.unhexlify('11B0282A189B75B0B4D2D8C7FA38548B')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    print('Not yet joined...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# send some data
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)
