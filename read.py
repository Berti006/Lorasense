import mfrc522
from os import uname
import pycom
import time

def do_read():
	pycom.heartbeat(False)
	# if uname()[0] == 'WiPy':
	# rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP14")
	# rdr = mfrc522.MFRC522("P14", "P16", "P15", "P22", "P14")
	rdr = mfrc522.MFRC522("P7", "P9", "P8", "P11", "P12")
	# elif uname()[0] == 'esp8266':
	# rdr = mfrc522.MFRC522(14, 16, 15, 22, 14)
	# else:
	# 	raise RuntimeError("Unsupported platform")

	print("")
	print("Place card before reader to read from address 0x08")
	print("")

	try:
		while True:
			pycom.rgbled(0x000000)

			(stat, tag_type, recv) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")
					pycom.rgbled(0xff00ff)

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Address 8 data: %s" % rdr.read(8))
							rdr.stop_crypto1()
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")
			# else:
			# 	print("Something wrong")
			# 	print("  Status: " + str(stat))
			# 	print("Tag Type: " + str(tag_type))
			# 	print("    recv: " + str(recv))

			time.sleep(0.7)
	except KeyboardInterrupt:
		print("Bye")
