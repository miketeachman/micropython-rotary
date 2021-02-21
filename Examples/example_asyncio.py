# The MIT License (MIT)
# Copyright (c) 2021 Junliang Yan
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
# - uasyncio implementation

import sys
if sys.platform == 'esp8266' or sys.platform == 'esp32':
    from rotary_irq_esp import RotaryIRQ
elif sys.platform == 'pyboard':
    from rotary_irq_pyb import RotaryIRQ
else:
    print('Warning:  The Rotary module has not been tested on this platform')

import uasyncio as asyncio
from machine import Pin


# Use heartbeat to keep event loop not empty
async def heartbeat():
    while True:
        await asyncio.sleep_ms(10)

event = asyncio.Event()


def callback():
    event.set()


async def main():
    r = RotaryIRQ(pin_num_clk=14,
                  pin_num_dt=15)
    r.add_listener(callback)
    
    asyncio.create_task(heartbeat())
    while True:
        await event.wait()
        print('result =', r.value())
        event.clear()

try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print('Exception {} {}\n'.format(type(e).__name__, e))
finally:
    ret = asyncio.new_event_loop()  # Clear retained uasyncio state
