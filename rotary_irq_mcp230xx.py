# The MIT License (MIT)
# Copyright (c) 2024 Daniel Siegmanski
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# mcp23017 implementation

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from .rotary import Rotary
from machine import Pin

class RotaryIRQ(Rotary): 
    
    def __init__(self, mcp, pin_num_clk, pin_num_dt, pin_num_int, min_val=0, max_val=10, incr=1,
                 reverse=False, range_mode=Rotary.RANGE_UNBOUNDED, pull_up=False, half_step=False, invert=False):
        
        super().__init__(min_val, max_val, incr, reverse, range_mode, half_step, invert)
        
        self.mcp = mcp
        self.clk = pin_num_clk
        self.dt = pin_num_dt

        ### Configure MCP23017 ###
        # Set CLK and DT pin as input
        self.mcp.setup(self.clk, 1)
        self.mcp.setup(self.dt, 1)
		# enable pull ups
        if pull_up:
            self.mcp.pullup(self.clk, True)
            self.mcp.pullup(self.dt, True)
        # enable interrupt
        self.mcp.set_interrupt(self.clk, True)
        self.mcp.set_interrupt(self.dt, True)
        self.mcp.configure(interrupt_polarity=True)
        
		# interrupt pin, set as input
        self.int_pin = Pin(pin_num_int, Pin.IN)
        self.int_pin.irq(trigger=self.int_pin.IRQ_RISING, handler=self._process_rotary_pins)
        
    def _hal_get_clk_value(self):
        return self.mcp.read_captured_gpio()[self.clk]
        
    def _hal_get_dt_value(self):
        return self.mcp.read_captured_gpio()[self.dt]

    def _hal_close(self):
        self.int_pin.irq(handler=None)