from usbtmcDevice import UsbtmcDevice
import os
import time

d_path = 'figs/'
dev_scope = UsbtmcDevice('/dev/usbtmc0')

def get_data(fname):
    get_display(fname)
    get_data(fname)

def get_display(fname):
    dev_scope.write(':display:data? on,off,png')
    time.sleep(1)
    buf = dev_scope.read()
    img_data = strip_hdr(buf)
    fd = os.open(d_path + fname + '.png', os.O_CREAT | os.O_WRONLY)
    os.write(fd, img_data)
    os.close(fd)

def get_wave(fname, ch='1'):
    dev_scope.write('WAV:SOUR CHAN'+ch)
    buf = dev_scope.ask('wav:data?')
    data = strip_hdr(buf)

    yref = float(dev_scope.ask('wav:yref?'))
    yinc = float(dev_scope.ask('wav:yinc?'))
    yori = float(dev_scope.ask('wav:yorigin?'))
    tbase = float(dev_scope.ask('timebase:scale?'))
    print('[yref, yinc, yori, tbase] =', [yref, yinc, yori, tbase])

    samples = [((s-yref)-yori)*yinc for s in data]
    fd = os.open(d_path + fname + '.param', os.O_CREAT | os.O_WRONLY)
    os.write(fd, str([yref, yinc, yori, tbase]))
    os.close(fd)
    return data, samples, tbase

def strip_hdr(data):
    assert data[0] == '#'
    h_len = int(data[1])
    s_num = int(data[2:2+h_len])
    print('data_hdr: ' + data[0:2+h_len])
    return bytearray(data[h_len+2:h_len+2+s_num])



get_data('zad_3')