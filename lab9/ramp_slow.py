from machine import Pin
def start():
    scl = Pin(5, Pin.OUT)
    sda = Pin(4, Pin.OPEN_DRAIN)
    return scl, sda

def shift(sda):
    addr = [1,0,0,1,1,1,1]
    mode = 1
    for bit in addr:
        sda(bit)
    sda(mode)

def stop(scl):
    return scl()


scl, sda = start()
shift(sda)
print(scl())
