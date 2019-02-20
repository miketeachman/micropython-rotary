# The MIT License (MIT)
# Copyright (c) 2018 Mike Teachman
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# ESP8266/ESP32 implementation
# ESP32 has IRQs on all Pins

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin
from rotary import Rotary
from sys import platform

_rotary_pins = [4, 5, 12, 13, 14]

class RotaryIRQ(Rotary): 
    
    def __init__(self, pin_num_clk, pin_num_dt, min_val=0, max_val=10, reverse=False, range_mode = Rotary.RANGE_UNBOUNDED):
        
        if platform != 'esp32':
            if not pin_num_clk in _rotary_pins:
                raise ValueError
            if not pin_num_dt in _rotary_pins:
                raise ValueError            

        self._pin_clk = Pin(pin_num_clk, Pin.IN)
        self._pin_dt = Pin(pin_num_dt, Pin.IN)
        super().__init__(min_val, max_val, reverse, range_mode)
        self._enable_clk_irq(self._process_rotary_pins)        
        self._enable_dt_irq(self._process_rotary_pins)   
        
    def _enable_clk_irq(self, callback=None):
        self._pin_clk.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)
        
    def _enable_dt_irq(self, callback=None):
        self._pin_dt.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)
        
    def _disable_clk_irq(self):
        self._pin_clk.irq(handler=None)
        
    def _disable_dt_irq(self):
        self._pin_dt.irq(handler=None)     
    
    def _hal_get_clk_value(self):
        return self._pin_clk.value()
        
    def _hal_get_dt_value(self):
        return self._pin_dt.value()        

    def _hal_close(self):
        self._disable_clk_irq()
        self._disable_dt_irq()  
        