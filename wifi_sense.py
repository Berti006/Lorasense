import pycom
import network
from network import LoRa
from network import WLAN
import binascii

mac = binascii.hexlify(network.LoRa().mac())


print("*************************************")
print("     LoraSense 0.1")
print("")
print("MAC: " + mac.upper().decode('utf-8'))
print("*************************************")

pycom.heartbeat(False)
pycom.rgbled(0x000000)

wifi_adapter = WLAN(mode=WLAN.STA)
print("Wifi Mode: " + str(wifi_adapter.mode()))

nets = wifi_adapter.scan()
for net in nets:
    print(net.ssid)
