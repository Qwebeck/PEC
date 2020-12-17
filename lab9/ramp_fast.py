# picocom /dev/ttyUSB0 -b115200
# http://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c

from machine import Pin, I2C

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
addr = 0x48

def ramp():
	i2c.start()
	i2c.writeto(addr, b'\x40', 0) #D/A enable
	buf = bytearray(1)
	x = 0
	while(1):
		buf[0] = x
		i2c.write(buf)
		x+=1


# http://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
def adc(): 
	while(1): 
		x = i2c.readfrom(addr, 1, 0) 
		print(x[0])







