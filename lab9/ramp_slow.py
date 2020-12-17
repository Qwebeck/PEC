# picocom /dev/ttyUSB0 -b115200

from machine import Pin

scl = Pin(5, Pin.OUT)
sda = Pin(4, Pin.OPEN_DRAIN)

addr = 0x48

def start():
	scl.value(1)
	sda.value(1)
	sda.value(0)
	scl.value(0)


def shift(x):
	for n in range(8):
		b = (x >> 7) & 1
		#print(b)
		sda.value(b)
		x <<= 1
		scl.value(1)
		scl.value(0)
	sda.value(1)
	scl.value(1)
	ack=sda.value()
	scl.value(0)
	return ack


def ramp():
	start()
	shift(addr<<1)  #address
	shift(0x40)  #D/A enable
	x=0
	while(1):
		shift(x)
		x+=1


ramp()




