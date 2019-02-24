# MicroPython Rotary Encoder Driver
A MicroPython driver to read a rotary encoder.  This is a robust implementation that uses two GPIO pins configured to trigger an interrupt, following Ben Buxton's implementation:
* http://www.buxtronix.net/2011/10/rotary-encoders-done-properly.html
* https://github.com/buxtronix/arduino/tree/master/libraries/Rotary

<img src="https://user-images.githubusercontent.com/12716600/46682576-bfee3500-cba2-11e8-9bbe-0bd6e341b446.jpg" width="300">

Tested with:
* Adafruit Feather Huzzah ESP8266
* Adafruit Feather Huzzah ESP32 (credit:  implementation by @zoide)
* KY-040 rotary encoder
* MicroPython v1.9.4
* MicroPython v1.10

## Usage
install two MicroPython files using a file copy tool such as ampy, rshell, ...

```
ampy -pCOMx -d1 put rotary.py
ampy -pCOMx -d1 put rotary_irq_esp.py
```

import class

```
from rotary_irq_esp import RotaryIRQ
```

initialize

```
r = RotaryIRQ(pin_num_clk, 
              pin_num_dt, 
              [min_val=0], 
              [max_val=10], 
              [reverse=False], 
              [range_mode=RotaryIRQ.RANGE_UNBOUNDED])
              
```
read encoder

```
value = r.value()
```

reset encoder to min_val

```
r.reset()
```

deactivate microcontroller pins used to read encoder  

```  
r.close                  
```
    

### RotaryIRQ() Arguments
| argument       | description           | value |
|-------------|-------------|---------|
| pin_num_clk      | GPIO pin connected to encoder CLK pin| integer |
| pin_num_dt     | GPIO pin connected to encoder DT pin      |  integer |
| min_val | minimum value in the encoder range. Also the starting value |  integer |
| max_val | maximum value in the encoder range (not used when range_mode = RANGE_UNBOUNDED)      | integer |
| reverse | reverse count direction | True or False(default) |
| range_mode | count behavior at min_val and max_val       | RotaryIRQ.RANGE_UNBOUNDED(default) RotaryIRQ.RANGE_WRAP RotaryIRQ.RANGE_BOUNDED |


| range_mode | description |
| ------------- | ------------- |
| RotaryIRQ.RANGE_UNBOUNDED | encoder has no bounds on the counting range |
| RotaryIRQ.RANGE_WRAP | encoder will count up to max_val then wrap to minimum value (similar behaviour for count down) |
| RotaryIRQ.RANGE_BOUNDED |  encoder will count up to max_val then stop.  Count down stops at min_val |

## Example
* CLK pin attached to GPIO14
* DT pin attached to GPIO13
* GND pin attached to GND
* \+ pin attached to 3.3V
* Range mode = RotaryIRQ.RANGE_WRAP
* Range 0...5

* For clockwise turning the encoder will count 0,1,2,3,4,5,0,1 ...
* For counter-clockwise turning the encoder will count 0,5,4,3,2,1,0,5,4 ....

```
import time
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=14, 
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
```
          

### Rotary Encoder Wiring
| Encoder Pin       | Connection           | 
| ------------- |:-------------:| 
| +      | 3.3V | 
| GND     | Ground      |  
| DT | GPIO pin      |  
| CLK | GPIO pin      | 

## ESP8266 input pins
This Rotary module requires pins that support interrupts.  The following ESP8266 GPIO pins are recommended for this rotary encoder module
*   GPIO4 
*   GPIO5
*   GPIO12
*   GPIO13
*   GPIO14

The following ESP8266 GPIO pins are **not recommended** for use with this module.
*   GPIO0 - used to detect boot-mode.  Bootloader runs when pin is low during powerup.
*   GPIO2 - used to detect boot-mode.  Attached to pull-up resistor.
*   GPIO15 - used to detect boot-mode.  Attached to pull-down resistor.
*   GPIO16 - does not support interrupts.

## ESP32 input pins
This Rotary module requires pins that support interrupts.  All ESP32 GPIO pins support interrupts.
 
The following ESP32 GPIO strapping pins are **not recommended** for use with this module.
*   GPIO0 - used to detect boot-mode.  Bootloader runs when pin is low during powerup. Internal pull-up resistor.
*   GPIO2 - used to enter serial bootloader.  Internal pull-down resistor.
*   GPIO4 - technical reference indicates this is a strapping pin, but usage is not described.  Internal pull-down resistor.
*   GPIO5 - used to configure SDIO Slave.  Internal pull-up resistor.
*   GPIO12 - used to select flash voltage.  Internal pull-down resistor.
*   GPIO15 - used to configure silencing of boot messages.  Internal pull-up resistor.

## Implementation Details

The driver is split into two parts:
1. Platform-independent file:   rotary.py
2. Platform-dependent file:  rotary_irq_esp.py  (interrupt implementation for ESP8266 and ESP32)

CLK and DT transitions captured on an oscilloscope.  CLK = Yellow. DT = Blue

One clockwise step
![cw](https://user-images.githubusercontent.com/12716600/46682621-e44a1180-cba2-11e8-98b5-9dc2368e1635.png)

One counter-clockwise step
![ccw](https://user-images.githubusercontent.com/12716600/46682653-fe83ef80-cba2-11e8-9a2a-b6ee1f3bdee7.png)

## Acknowlegements
This MicroPython implementation is an adaptation of Ben Buxton's C++ work:  
* https://github.com/buxtronix/arduino/tree/master/libraries/Rotary

Other implementation ideas and techniques taken from:
* https://github.com/SpotlightKid/micropython-stm-lib/tree/master/encoder
* https://www.youtube.com/watch?v=BJHftzjNjkw
* https://github.com/dhylands/python_lcd
        
## Future Ambitions
* polling mode
* uasyncio example
* add tests