# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
#
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from rotary_irq_esp import RotaryIRQ
import uasyncio as aio
from uasyncio import Event
from machine import Pin

# Use heartbeat to keep event loop not empty
async def heartbeat():
    led = Pin(2, Pin.OUT);
    while True:
        led.on();
        await aio.sleep(0.1);
        led.off();
        await aio.sleep(0.8);

event = Event()

def callback():
    event.set()

async def handler():
    r = RotaryIRQ(pin_num_clk=27,
                  pin_num_dt=26)

    r.add_listener(callback)
    while True:
        await event.wait()
        print('result =', r.value())
        event.clear()

def main():
    aio.run(aio.gather(handler(), heartbeat()))

main()
print("it should not go here.")
