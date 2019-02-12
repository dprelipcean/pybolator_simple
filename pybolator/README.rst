===========
 pybolator
===========

PyBoard emulator

.. note:: very early development state

Features
========

- Allows minor testing of micropython code without an actual pyboard.
- Simulate hardware interaction from a script.
- Contains Pins configuration.

Usage
=======
Include the following import structure:



```python
    try:
        import pyb
    except ModuleNotFoundError:
        import tests.emulators.pybolator.pyboard as pyb
        print("Run pyb as mock.")
```


Supported methods and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Time related functions
++++++++++++++++++++++

- delay(ms)
- udelay(us)



Class pyb.Accel
+++++++++++++++

Methods
#######

- accel.x()
- accel.y()


Class pyb.ADC
+++++++++++++

Methods
#######

- adc.read()
- adc.read_timed()

Class pyb.LCD
+++++++++++++

Methods
#######

- lcd(skin_position)
- lcd.contrast(value)
- lcd.fill(colour)
- lcd.get(x, y)
- lcd.light(value)
- lcd.pixel(x, y, colour)
- lcd.show()
- lcd.text(str, x, y, colour)
- lcd.write(str)

Class pyb.ExtInt
++++++++++++++++

Methods
#######

- extint.disable()
- extint.enable()

Class pyb.DAC
+++++++++++++

Methods
#######

- dac.write_timed()
- dac.write()

Class pyb.I2C
+++++++++++++

Methods
#######

- i2c.init()
- i2c.is_ready()
- i2c.recv()
- i2c.send()
- i2c.scan()

Class pyb.LED
+++++++++++++

Methods
#######

- led.intensity([value])
- led.off()
- led.on()
- led.toggle()

Class pyb.Pin
+++++++++++++

Methods
#######
- pin.debug()
- pin.dict()
- pin.mapper()
- pin.init()
- pin.value()
- pin.name()
- pin.pull()


Class pyb.SPI
+++++++++++++

Methods
#######

- spi.send()
- spi.recv()
- spi.send_recv()

Class pyb.Switch
++++++++++++++++

Methods
#######

- switch()
- switch.callback(fun)

Class pyb.Timer
++++++++++++++++

Methods
#######

- timer.counter()
- timer.freq()
- timer.period()
- timer.prescaler()
- timer.source_freq()

Class pyb.TimerChannel
+++++++++++++++

Methods
#######

- timerchannel.pulse_width_percent()

Class pyb.UART
+++++++++++++++

Methods
#######

- uart.any()
- uart.read()
- uart.write()
- uart.writerchar()

Unsupported methods and classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reset related functions
+++++++++++++++++++++++

- bootloader()

Interrupt related functions
+++++++++++++++++++++++++++

- disable_irq()
- enable_irq(state=True)

Power related functions
+++++++++++++++++++++++

- freq([sysclk[, hclk[, pclk1[, pclk2]]]])
- wfi()
- stop()
- standby()

Miscellaneous functions
+++++++++++++++++++++++

- have_cdc()
- hid((buttons, x, y, z))
- info([dump_alloc_table])
- main(filename)
- mount(device, mountpoint, \*, readonly=False, mkfs=False)
- repl_uart(uart)
- rng()
- sync()
- unique_id()

Class pyb.Accel
+++++++++++++++

Methods
#######

- accel.filtered_xyz()
- accel.tilt()
- accel.z()

Class pyb.ADCAll
+++++++++++++


Class pyb.CAN
+++++++++++++

Class pyb.DAC
+++++++++++++

Methods
#######

- dac.init()
- dac.deinit()
- dac.noise()
- dac.triangle()

Class pyb.ExtInt
++++++++++++++++

Methods
#######

- extint.line()
- extint.swint()


Class pyb.I2C
+++++++++++++

Methods
#######

- i2c.deinit()
- i2c.mem_read()
- i2c.mem_write()

Class pyb.LCD
+++++++++++++

Methods
#######

- lcd.command(instr_data, buf)


Class pyb.Pin
+++++++++++++

Methods
#######

- pin.af()
- pin.af_list()
- pin.gpio()
- pin.names()
- pin.pin()
- pin.port()

Class pyb.PinAF
+++++++++++++


Class pyb.RTC
+++++++++++++

Class pyb.Servo
+++++++++++++++

Class pyb.SPI
+++++++++++++

Methods
#######

- spi.deinit()
- spi.init()

Class pyb.Timer
+++++++++++++++

Methods
#######

- timer.init()
- timer.deinit()
- timer.callback()

Class pyb.TimerChannel
+++++++++++++++

Methods
#######

- timerchannel.capture()
- timerchannel.compare()
- timerchannel.pulse_width()

Class pyb.UART
+++++++++++++++

Methods
#######

- uart.init()
- uart.deinit()
- uart.readchar()
- uart.readinto()
- uart.readline()
- uart.sendbreak()


Class pyb.USB_VCP
+++++++++++++++++


