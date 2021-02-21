# The MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder

import sys
if sys.platform == 'esp8266' or sys.platform == 'esp32':
    from rotary_irq_esp import RotaryIRQ
elif sys.platform == 'pyboard':
    from rotary_irq_pyb import RotaryIRQ
else:
    print('Warning:  The Rotary module has not been tested on this platform')

import time
import uasyncio as asyncio
from machine import Pin

r = RotaryIRQ(pin_num_clk=14,
              pin_num_dt=15,
              min_val=0,
              max_val=5,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)

val_old = r.value()
while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    time.sleep_ms(50)
