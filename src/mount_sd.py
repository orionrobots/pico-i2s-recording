from machine import Pin, SPI
import sdcard
import os
import ucontextlib

def mount():
    sd_spi = SPI(0, 10_000_000,
                        sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    sd = sdcard.SDCard(spi=sd_spi, cs=Pin(1))
    os.mount(sd, "/sd")
    return sd

def unmount():
    os.umount("/sd")

@ucontextlib.contextmanager
def sd_mounted():
    sd = mount()
    try:
        yield
    finally:
        os.umount("/sd")
