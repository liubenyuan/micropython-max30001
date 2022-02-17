# liubenyuan <liubenyuan@gmail.com>
from machine import SPI, Pin
import struct


# https://docs.python.org/3/library/struct.html
def int2bytes(d):
    return struct.pack(">I", d)


def bytes2short(d):
    val = struct.unpack(">I", d)[0]
    btal = val & 0x7
    bioz_adc = val >> 4

    vref = 1.0
    bioz_cmag = 32e-6
    bioz_gain = 10
    bioz = bioz_adc * vref / (2**19 * bioz_cmag * bioz_gain)
    return bioz, btal


# liubenyuan 2021/11/26
class MAX30001(object):
    def __init__(self, spi, ss):
        self.spi = spi
        self.ss = ss

    def write(self, addr, data):
        """addr is the address, data is 32 bit unsigned int (hex)"""
        self.ss.off()
        buf = [0, 0, 0, 0]
        buf[0] = (addr << 1) | 0x0
        buf[1] = (data >> 16) & 0xFF
        buf[2] = (data >> 8) & 0xFF
        buf[3] = data & 0xFF
        self.spi.write(bytes(buf))
        self.ss.on()

        return 0

    def read(self, addr):
        self.ss.off()
        tx_buf = bytes([(addr << 1) | 0x1, 0, 0, 0])
        rx_buf = bytearray(4)
        self.spi.write_readinto(tx_buf, rx_buf)
        self.ss.on()

        return rx_buf


# spi = SPI(1, 1000000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
spi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
ss = Pin(22, Pin.OUT)
ss.on()
max3 = MAX30001(spi, ss)

# how to write
addr = 0x10
d = 0x040027
max3.write(addr, d)

addr = 0x17
# d = 0x001040
d = 0x001840  # BIST
max3.write(addr, d)

addr = 0x18
d = 0x201130  # BIOZ_CGMAG=0x3, 32 uA, BIOZ_GAIN=0x0, 10
max3.write(addr, d)

# how to read
addr = 0x23
rx_buf = max3.read(addr)
print(rx_buf)

# how to convert
val = bytes2short(rx_buf)
print(val)
