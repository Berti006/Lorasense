import pycom
import network
from network import LoRa
import binascii

mac = binascii.hexlify(network.LoRa().mac())


print("*************************************")
print("     LoraSense 0.1")
print("")
# print("MAC: " + mac)
print("*************************************")

pycom.heartbeat(False)
pycom.rgbled(0x000000)
