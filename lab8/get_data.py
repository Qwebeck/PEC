#	ssh -p2221 student@149.156.197.221
#	sftp -P2221 student@149.156.197.221

from __future__ import division
from __future__ import print_function

import time
import os

from usbtmcDevice import UsbtmcDevice

d_path = 'figs/'

# connect to instruments
dev_scope = UsbtmcDevice('/dev/usbtmc0')
id = dev_scope.ask('*idn?')
print(id)

dev_scope.write('chan1:disp on')
dev_scope.write('chan1:probe 10')
dev_scope.write('chan1:coupling DC')
dev_scope.write('chan1:scale 0.5')
dev_scope.write('chan1:offset -1.5')
dev_scope.write('timebase:scale 1e-4')
dev_scope.write(':TRIGger:SWEep Auto')
dev_scope.write(':TRIGger:EDGe:LEVel 0.5')

dev_scope.write('chan2:disp on')
dev_scope.write('chan2:probe 1')

dev_gen = UsbtmcDevice('/dev/usbtmc1')
id = dev_gen.ask('*idn?')
print(id)


def strip_hdr(data):
    assert data[0] == '#'
    h_len = int(data[1])
    s_num = int(data[2:2+h_len])
    print('data_hdr: ' + data[0:2+h_len])
    return bytearray(data[h_len+2:h_len+2+s_num])


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


def get_data2(duty, offset, coupling, scale):
    fname = 'SQ_' + coupling + '_' + str(offset) + 'V_' + str(duty) + '%'
    print(fname)
    dev_scope.write('chan2:coupling ' + coupling)
    dev_scope.write('chan2:offset ' + str(offset))
    dev_scope.write('chan2:scale ' + str(scale))
    time.sleep(1)
    get_display(fname)

    dev_scope.write('WAV:SOUR CHAN2')
    time.sleep(1)
    [data, samples, tbase] = get_wave(fname, '2')
    fd = os.open(d_path + fname + '.raw', os.O_CREAT | os.O_WRONLY)
    os.write(fd, data)
    os.close(fd)


def SQ_test():
    freq = 2000
    lo = 0
    hi = 4
    duty = 20
    gen_squ(freq, lo, hi, duty)
    get_data2(duty, offset=-2, coupling='DC', scale=1)
    get_data2(duty, offset=0, coupling='AC', scale=1)

    duty = 80
    gen_squ(freq, lo, hi, duty)
    get_data2(duty, offset=-2, coupling='DC', scale=1)
    get_data2(duty, offset=0, coupling='AC', scale=1)


def Z5():
    freq = 1e5
    lo = 0
    hi = 4
    duty = 50
    gen_squ(freq, lo, hi, duty)
    dev_scope.write(':TRIGger:EDGe:SOURce CHANnel2')

    get_display('test')
    dev_scope.write('timebase:scale 1e-8')
    get_display('test')


def gen_squ(freq, lo, hi, duty):
    off = 0
    dev_gen.write('output off')
    dev_gen.write('func squ')
    dev_gen.ask('func?')
    dev_gen.write('freq %f' % freq)
    dev_gen.write('func:squ:dcyc %f' % duty)

    dev_gen.write('volt:offs %f' % off)
    print('volt:offs? ' + dev_gen.ask('volt:offs?'))
    time.sleep(1)

    dev_gen.write('volt:low %f' % lo)
    print('volt:low? ' + dev_gen.ask('volt:low?'))
    time.sleep(1)

    dev_gen.write('volt:high %f' % hi)
    print('volt:high? ' + dev_gen.ask('volt:high?'))
    time.sleep(1)

    dev_gen.write('output on')
    time.sleep(1)


def gen_sin(freq, vpp):
    freq = 1000
    vpp = 10
    offset = 0

    dev_gen.write('output off')
    dev_gen.write('func sin')
    dev_gen.write('freq %f' % freq)
    dev_gen.write('volt %f' % vpp)
    dev_gen.write('volt:offs %f' % offset)
    dev_gen.write('output on')


get_display('test')

if __name__ == '__main__':
    get_data2(50, 0, 'DC', 1)
    get_data2(80, 0, 'DC', 1)
