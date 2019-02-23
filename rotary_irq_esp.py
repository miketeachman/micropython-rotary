# The MIT License (MIT)
# Copyright (c) 2019 Mike Teachman
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# ESP8266/ESP32 implementation
# ESP32 has IRQs on all Pins

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin
from rotary import Rotary
from sys import platform

_esp8266_whitelist_pins = [4, 5, 12, 13, 14]
_esp32_blacklist_pins = [0, 2, 4, 5, 12, 15]

class RotaryIRQ(Rotary): 
    
    def __init__(self, pin_num_clk, pin_num_dt, min_val=0, max_val=10, reverse=False, range_mode = Rotary.RANGE_UNBOUNDED):
        
        if platform == 'esp32':
            if pin_num_clk in _esp32_blacklist_pins:
                raise ValueError('%s: Pin %d not allowed. Blacklist: %s' % (platform, pin_num_clk,_esp32_blacklist_pins))
            if pin_num_dt in _esp32_blacklist_pins:
                raise ValueError('%s: Pin %d not allowed. Blacklist: %s' % (platform, pin_num_dt,_esp32_blacklist_pins))
        else:
            if not pin_num_clk in _esp8266_whitelist_pins:
                raise ValueError('%s: Pin %d not allowed. Whitelist: %s' % (platform, pin_num_dt,_esp8266_whitelist_pins))
            if not pin_num_dt in _esp8266_whitelist_pins:
                raise ValueError('%s: Pin %d not allowed. Whitelist: %s' % (platform, pin_num_dt,_esp8266_whitelist_pins))            

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
        