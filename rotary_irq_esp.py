# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# ESP8266/ESP32 implementation

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin
from rotary import Rotary
from sys import platform

_esp8266_deny_pins = [16]


class RotaryIRQ(Rotary):

    def __init__(self, pin_num_clk, pin_num_dt, min_val=0, max_val=10,
                 reverse=False, range_mode=Rotary.RANGE_UNBOUNDED, pull_up=False, half_step=False):

        if platform == 'esp8266':
            if pin_num_clk in _esp8266_deny_pins:
                raise ValueError(
                    '%s: Pin %d not allowed. Not Available for Interrupt: %s' %
                    (platform, pin_num_clk, _esp8266_deny_pins))
            if pin_num_dt in _esp8266_deny_pins:
                raise ValueError(
                    '%s: Pin %d not allowed. Not Available for Interrupt: %s' %
                    (platform, pin_num_dt, _esp8266_deny_pins))

        super().__init__(min_val, max_val, reverse, range_mode, half_step)

        if pull_up == True:
            self._pin_clk = Pin(pin_num_clk, Pin.IN, Pin.PULL_UP)
            self._pin_dt = Pin(pin_num_dt, Pin.IN, Pin.PULL_UP)
        else:
            self._pin_clk = Pin(pin_num_clk, Pin.IN)
            self._pin_dt = Pin(pin_num_dt, Pin.IN)

        self._enable_clk_irq(self._process_rotary_pins)
        self._enable_dt_irq(self._process_rotary_pins)

    def _enable_clk_irq(self, callback=None):
        self._pin_clk.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=callback)

    def _enable_dt_irq(self, callback=None):
        self._pin_dt.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=callback)

    def _disable_clk_irq(self):
        self._pin_clk.irq(handler=None)

    def _disable_dt_irq(self):
        self._pin_dt.irq(handler=None)

    def _hal_get_clk_value(self):
        return self._pin_clk.value()

    def _hal_get_dt_value(self):
        return self._pin_dt.value()

    def _hal_enable_irq(self):
        self._enable_clk_irq(self._process_rotary_pins)
        self._enable_dt_irq(self._process_rotary_pins)

    def _hal_disable_irq(self):
        self._disable_clk_irq()
        self._disable_dt_irq()

    def _hal_close(self):
        self._hal_disable_irq()
