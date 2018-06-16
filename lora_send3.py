import socket
import binascii
import struct
import time
import pycom
import network
from network import LoRa
from network import WLAN

class LoraSender():
    def __init__(self, node_id, sec_key):
        mac = binascii.hexlify(network.LoRa().mac())

        print("*************************************")
        print("     LoraSense 0.1")
        print("")
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
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

        # create an ABP authentication params
        dev_addr = struct.unpack(">l", binascii.unhexlify('%08d' % node_id))[0]
        nwk_swkey = binascii.unhexlify(sec_key)
        app_swkey = binascii.unhexlify(sec_key)

        # join a network using ABP (Activation By Personalization)
        self.lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

        # create a LoRa socket
        self.sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        self.sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        self.msgCnt = 0

    def send_msg(self, msg):
        print("Sending JSON data")
        pycom.rgbled(0xff0000)
        # send some data
        self.msgCnt += 1
        print("Sending: " + msg)
        self.sock.setblocking(True)
        self.sock.send(msg)
        print("Message sent!")
        self.sock.setblocking(False)
        pycom.rgbled(0x000000)

if __name__ == "__main__":
    sender = LoraSender(1, '2B7E151628AED2A6ABF7158809CF4F3C')
    while True:
        jdata = """
        { "node" : "Lorasense",
          "nodeID" : "0001",
          "msgID" : %d,
          "count" : [42 42 42]}""" % str(sender.msgCnt)
        sender.send_msg(jdata)
        time.sleep(60)
