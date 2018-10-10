# The MIT License (MIT)
# Copyright (c) 2018 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
#
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

import time
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=12, 
              pin_num_dt=13, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
lastval = r.value()
while True:
    val = r.value()
    
    if lastval != val:
        lastval = val
        print('result =', val)
        
    time.sleep_ms(50)