# MicroPython ST7735 TFT display driver example usage

import gc
from machine import Pin, SPI
from tft import TFT_GREEN
gc.collect()
import font
import network, socket

# DC       - RS/DC data/command flag
# CS       - Chip Select, enable communication
# RST/RES  - Reset
dc  = Pin(2, Pin.OUT)
cs  = Pin(0, Pin.OUT)
rst = Pin(16, Pin.OUT)
# SPI Bus (CLK/MOSI/MISO)
# check your port docs to see which Pins you can use
spi = SPI(1, baudrate=8000000, polarity=0, phase=0)

# TFT object, this is ST7735R green tab version
tft = TFT_GREEN(128, 160, spi, dc, cs, rst, rotate=90)

# init TFT
tft.init()

#Network
sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)
sta.active(True)
sta.connect("YOUR_SSID_HERE", "YOUR_PASSWORD_HERE")
while not sta.isconnected():
    pass
print(sta.ifconfig())
ap.active(False)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = socket.getaddrinfo("0.0.0.0", 23)[0][-1]
s.bind(addr)
s.listen(1)

tft.clear(tft.rgbcolor(0, 0, 0)) #b, g, r
tft.text(0,0,"Test", font.terminalfont, tft.rgbcolor(255, 255, 255), 2)
r, a = s.accept()
tft.text(0,0,"Test", font.terminalfont, tft.rgbcolor(0, 0, 0), 2)
old = " "
while True:
    d = r.recv(1024).decode("utf-8")
    if d[0:8] == "rotation":
        ro = int(d[9:12])
        tft.changeRotate(ro)
        continue
    print(d)
    tft.text(0,0,old, font.terminalfont, tft.rgbcolor(0, 0, 0), 2)
    tft.text(0,0,d, font.terminalfont, tft.rgbcolor(255, 255, 255), 2)
    old = d


#tft.pixel(127, 159, tft.rgbcolor(250,0,0))
