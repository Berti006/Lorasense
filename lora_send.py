import pycom
from network import LoRa
import socket
import machine
import time

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setblocking(True)
s.send('{ "node" : "LoraSense"}')
s.setblocking(False)
data.s.recv(64)
print(data)
