#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Coded by aqil.almara

import os;
import time;

if os.name=='nt':
    os.system('cls && color 0A && mode 25,4');
else: print('\r\x1b[0;1;92m', end='\r');

class ClAss:

    def __init__(self):
        self.ReturN;

    def DaTez_Kun(self, teks):
        for o in teks+'\n':
            print(o, end='', flush=True);
            time.sleep(.1);

    @property
    def ReturN(self):
        for _ in range(9, -1, -1):
            print(f"\r [*] Wait a Second! {_} ", end='', flush=True);
            time.sleep(.95);
        self.DaTez_Kun('\n [*] Thanks For Waiting');

if __name__ == '__main__':
    ClAsss();
