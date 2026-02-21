# MIT License (MIT)
# Copyright (c) 2024 Daniel Siegmanski
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder connecten at an MCP23017

from machine import I2C
import mcp #MCP module from https://github.com/dsiggi/micropython-mcp230xx
from rotary_irq_mcp230xx import RotaryIRQ
import time

i2c = I2C(0)
io = mcp.MCP23017(i2c)

# CLK pin connected to mcp at GPIOA 0
# DT pin connected to mcp at GPIOA 1
# INTA pin from mcp connected to ESP pin 15

r = RotaryIRQ(mcp=io,
              pin_num_clk=0,
              pin_num_dt=1,
              pin_num_int=15,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)

val_old = r.value()
while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    time.sleep_ms(50)
