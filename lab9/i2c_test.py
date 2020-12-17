from machine import Pin

scl = Pin(5, Pin.OUT)
sda = Pin(4, Pin.OPEN_DRAIN)

addr_1 = 0x48
addr_2 = 0x49

def start():
	scl.value(1)
	sda.value(1)
	sda.value(0)
	scl.value(0)


def shift_out(x):
	for _ in range(8):
		b = (x >> 7) & 1
		print(b)
		sda.value(b)
		x <<= 1
		scl.value(1)
		scl.value(0)
	sda.value(1)
	scl.value(1)
	ack=sda.value()
	scl.value(0)
	return ack	


def scan():
    addr = []
    for i in range(256):
        if shift_out(i):
            addr.append(hex(i))
    return addr
    

#test address 1
start()
ack = shift_out((addr_1)<<1)
print ('ack:', ack)

#test address 2
start()
ack = shift_out((addr_2)<<1)
print ('ack:', ack)


print(scan())