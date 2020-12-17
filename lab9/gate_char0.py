# picocom /dev/ttyUSB0 -b115200

from machine import Pin, I2C

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
addr = 0x48

def adc(ch=2):
	i2c.start()
	buf = bytearray(1); buf[0] = 0x40 + ch
	i2c.writeto(0x48, buf) #D/A enable, ch
	x = i2c.readfrom(0x48, 2, 0); # print(x[1]);
	return x[1]


def dac(x):
	i2c.start()
	buf = bytearray(2)
	buf[0] = 0x40; buf[1] = x;
	i2c.writeto(0x48, buf) #D/A enable




