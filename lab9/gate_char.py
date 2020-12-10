from machine import Pin

scl = Pin(5, Pin.OUT)
sda = Pin(4, Pin.OPEN_DRAIN)

addr = [1,0,0,1,1,1,1]
mode = 1
p0 = Pin(2, Pin.IN)
for bit in p0:
    sda(bit)

ack = scl()
print(ack)
