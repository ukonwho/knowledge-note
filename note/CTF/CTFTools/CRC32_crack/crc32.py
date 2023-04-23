#!/usr/bin/env python
 
# -*- coding:utf-8 -*-
import datetime
import binascii
 
def showTime():
    print datetime.datetime.now().strftime("%H:%M:%S")  
 
def crack():
    crcs = set([0xc6a76f95])
    r = xrange(32, 127)
    for a in r:
        for b in r:
            for c in r:
                for d in r:
                    txt = chr(a)+chr(b)+chr(c)+chr(d)
                    crc = binascii.crc32(txt)
                    if (crc & 0xFFFFFFFF) in crcs:
                        print txt
 
 
if __name__ == "__main__":
    showTime()
    crack()
    showTime()