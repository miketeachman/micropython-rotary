"""Exercise real rotary state machines with simulated GPIO levels on a host."""
import builtins
import importlib
import sys
import types
import unittest
from unittest.mock import patch


class Pin:
    IN = PULL_UP = PULL_NONE = IRQ_RISING = 1
    IRQ_FALLING = 2
    levels = {}

    def __init__(self, number, *args):
        self.number = number

    def value(self, value=None):
        if value is not None:
            self.levels[self.number] = value
        return self.levels[self.number]

    def irq(self, *args, **kwargs):
        pass


class ExtInt:
    IRQ_RISING_FALLING = 3

    def __init__(self, *args):
        pass

    def enable(self):
        pass

    def disable(self):
        pass


class InitialStateTests(unittest.TestCase):
    def setUp(self):
        modules = {
            'micropython': types.ModuleType('micropython'),
            'machine': types.SimpleNamespace(Pin=Pin),
            'pyb': types.SimpleNamespace(Pin=Pin, ExtInt=ExtInt),
        }
        patcher = patch.dict(sys.modules, modules)
        patcher.start()
        self.addCleanup(patcher.stop)
        constants = patch.object(builtins, 'const', lambda value: value, create=True)
        constants.start()
        self.addCleanup(constants.stop)

    @staticmethod
    def levels(state, invert=False):
        physical = state ^ (3 if invert else 0)
        Pin.levels = {1: physical >> 1, 2: physical & 1}

    def test_first_half_step(self):
        for platform in ('rp2', 'esp', 'pyb'):
            driver = importlib.import_module('rotary_irq_' + platform)
            for start, steps in ((0, (1, 3, 2, 0)), (3, (2, 0, 1, 3))):
                for reverse in (False, True):
                    for invert in (False, True):
                        with self.subTest(platform=platform, start=start,
                                          reverse=reverse, invert=invert):
                            self.levels(start, invert)
                            encoder = driver.RotaryIRQ(1, 2, half_step=True,
                                                       reverse=reverse,
                                                       invert=invert)
                            observed = []
                            encoder.add_listener(lambda: observed.append(encoder.value()))
                            self.assertEqual(encoder.value(), 0)
                            for step in steps[:2]:
                                self.levels(step, invert)
                                encoder._process_rotary_pins(None)
                            increment = 1 if reverse else -1
                            self.assertEqual(encoder.value(), increment)
                            self.assertEqual(observed, [increment])
                            for step in steps[2:]:
                                self.levels(step, invert)
                                encoder._process_rotary_pins(None)
                            self.assertEqual(observed, [increment, 2 * increment])
                            encoder.close()

    def test_full_step_and_bounce(self):
        for platform in ('rp2', 'esp', 'pyb'):
            driver = importlib.import_module('rotary_irq_' + platform)
            for half, start, steps in ((False, 3, (2, 0, 1, 3)),
                                       (True, 0, (1, 0, 1, 3))):
                with self.subTest(platform=platform, half=half):
                    self.levels(start)
                    encoder = driver.RotaryIRQ(1, 2, half_step=half)
                    for step in steps:
                        self.levels(step)
                        encoder._process_rotary_pins(None)
                    self.assertEqual(encoder.value(), -1 if half else 1)
                    encoder.close()


if __name__ == '__main__':
    unittest.main()
