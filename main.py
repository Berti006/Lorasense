# main.py -- put your code here!

import mfrc522
from os import uname
import pycom
import time
import socket
import binascii
import struct
import network
from network import LoRa
from network import WLAN
from machine import Timer

# SETUP
mac = binascii.hexlify(network.LoRa().mac())


print("*************************************")
print("     LoraSense 0.1")
print("")
print("WiFi MAC: ")
print("LORA MAC: " + mac.upper().decode('utf-8'))
print("*************************************")

pycom.heartbeat(False)
pycom.rgbled(0x000000)
counts = [0,0,0]

rdr = mfrc522.MFRC522("P7", "P9", "P8", "P11", "P12")
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('00000001'))[0]
nwk_swkey = binascii.unhexlify('2B7E151628AED2A6ABF7158809CF4F3C')
app_swkey = binascii.unhexlify('2B7E151628AED2A6ABF7158809CF4F3C')

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)
msgCnt = 0

# LORA TRANSMIT TIMER
def lora_timer_tick(alarm):
    global msgCnt
    print("Sending JSON data")
    pycom.rgbled(0xff0000)
    # send some data
    msgCnt = msgCnt + 1
    jdata = '[{"node":"Lorasense","nodeID":"0001","msgID": ' + str(msgCnt) + ',"count":[' + str(counts[0]) + ',' + str(counts[1]) + ',' + str(counts[2]) + ']}]'
    print("Sending: " + jdata)
    s.setblocking(True)
    try:
        s.send(jdata)
    except OSError as e:
        pass
        # print("Error: " + e.args[0])
    pycom.rgbled(0xff00ff)
    s.setblocking(False)
    data = s.recv(64)
    print(data)
    pycom.rgbled(0x000000)
    counts[0] = counts[1]
    counts[1] = counts[2]
    counts[2] = 0

lora_timer = Timer.Alarm(lora_timer_tick, 60, periodic=True)

# MAIN READ LOOP
try:
    while True:
        pycom.rgbled(0x000000)
        (stat, tag_type, recv) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                pycom.rgbled(0xff00ff)
                counts[2] = counts[2] + 1
                print(counts)

        time.sleep(0.3)
except KeyboardInterrupt:
    print("Bye")
