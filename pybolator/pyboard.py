"""Pyboard emulator

@author: danielp
Based on existing draft from:
    github.com/alej0varas/pybolator"


Description:
    This script mock a pyboard, such that software can be tested w/o
    the hardware.

    In comparison to a completely mocked pyb module, this package
    interacts with the software as a pyboard would.

Usage inside scripts:
    import <path_to_package>.pybolator.pyboard as pyb
"""

# ======================================================================
# ========================= Import Statements ==========================
# ======================================================================

# # Built-in Imports:
import sys
from time import sleep
from random import randint

# # Third party imports:
from unittest.mock import Mock
# from datetime import datetime

# ======================================================================
# ============================== Script ================================
# ======================================================================


# ======================================================================
# ======================== Pyboard connections ===========================
# ======================================================================

PYBOARD_PINS = {
    "X1": {
        "status": "available",
        "role": "PWM",
        "usage": None,
    },

    "X2": {
        "status": "available",
        "role": "PWM",
        "usage": None,
    },

    "X3": {
        "status": "available",
        "role": "PWM",
        "usage": None,
    },

    "X4": {
        "status": "available",
        "role": "PWM",
        "usage": None,
    },

    "X5": {
        "status": "available",
        "role": "PWM",
        "usage": None,
    },

    "X6": {
        "status": "available",
        "role": "PWM",
        "usage": None,
    },
}


def _check_pin_availability(pin_name):
    """

    Parameters
    ----------
    pin_name: str

    Returns
    -------

    """
    if pin_name not in PYBOARD_PINS:
        raise Exception("Allocated Pin is not available on a pyboard.")

    if PYBOARD_PINS[pin_name]["status"] is not "available":
        usage = PYBOARD_PINS[pin_name]["usage"]
        error_message = "Allocated Pin is already used by {}.".format(usage)
        raise Exception(error_message)

    PYBOARD_PINS[pin_name]["status"] = "not available"
    return True

# ======================================================================
# ============================== Classes ================================
# ======================================================================


class Pin:
    """http://docs.micropython.org/en/latest/library/pyb.Pin.html"""

    # Mode constants
    AF_OD = 0
    AF_PP = 1
    ANALOG = 2

    IN = 3
    OUT = 4

    OUT_OD = 5
    OUT_PP = 6

    # Pull constants
    PULL_DOWN = 7
    PULL_NONE = 8
    PULL_UP = 8

    board = Mock()

    def __init__(self, pin_id, **kwargs):
        """Create a new Pin object associated with the id.

        If additional arguments are given, they are used to initialise
        the pin. See pin.init().

        Parameters
        ----------
        pin_id: str or int

        """

        _check_pin_availability(pin_id)
        self._id = pin_id

        # Init attributes
        if kwargs:
            self.init(kwargs)
        else:
            self._mode = None
            self._pull = None
            self._af = None

        self._pin_value = bool(0)  # This corresponds to pin down.

        # Attributes required/used in class methods
        self.debug_state = False
        self.pin_mapper_dict = {}
        self.pin_mapper_function = None

    def debug(self, state=None):
        """Get or set the debugging state (True or False for on or off).

        Parameters
        ----------
        state : bool

        Returns
        -------
        out : bool
        """
        if state is None:
            return self.debug_state
        else:
            self.debug_state = state

    def dict(self, pin_mapper_dict):
        """Get or set the pin mapper dictionary.

        Parameters
        ----------
        pin_mapper_dict: dict

        Returns
        -------
        out: dict
        """
        if pin_mapper_dict is None:
            return self.pin_mapper_dict
        else:
            self.pin_mapper_dict = pin_mapper_dict

    def mapper(self, func):
        """Get or set the pin mapper function.

        Parameters
        ----------
        func:

        Returns
        -------

        """
        if func is None:
            return self.pin_mapper_function
        else:
            self.pin_mapper_function = func

    def __str__(self):
        """Return a string describing the pin object."""
        return 'Emulated Pin object: {}'.format(self._id)

    def init(self, mode, pull=PULL_NONE, af=-1):
        """Initialise the pin:"""
        self._mode = mode
        self._pull = pull
        self._af = af

    def value(self, value=None):
        """Get or set the digital logic level of the pin.

        With value given,
            Set the logic level of the pin.


        Parameters
        ----------
        value
            Value can be anything that converts to a boolean.
            If it converts to True, the pin is set high,
            otherwise it is set low.


        Returns
        -------
        out : 0 or 1
            With no argument, depending on the logic level of the pin.
        """
        # sys.stderr.write("Pin value: {}\n".format(value))
        if value is not None:
            self._pin_value = bool(value)
        else:
            return self._pin_value

    def af(self):
        # Todo
        raise NotImplementedError()

    def af_list(self):
        """Returns an array of alternate functions available for this pin."""
        # Todo
        raise NotImplementedError()

    def gpio(self):
        """Returns the base address of the GPIO block of this pin."""
        # Todo
        raise NotImplementedError()

    def mode(self):
        """Returns the currently configured mode of the pin.

        The integer returned will match one of the allowed constants for
         the mode argument to the init function."""
        return self._mode

    def name(self):
        """Get the pin name."""
        # Todo:
        return self._id

    def names(self):
        """Returns the cpu and board names for this pin."""
        # Todo
        raise NotImplementedError()

    def pin(self):
        """Get the pin number."""
        # Todo
        raise NotImplementedError()

    def port(self):
        """Get the pin port."""
        # Todo
        raise NotImplementedError()

    def pull(self):
        """Returns the currently configured pull of the pin.

        The integer returned will match one of the allowed constants for
         the pull argument to the init function."""
        return self._pull


class ExtInt:

    IRQ_FALLING = 270598144
    IRQ_RISING = 269549568
    IRQ_RISING_FALLING = 271646720

    def __init__(self, pin, mode, pull, callback):
        """

        Parameters
        ----------
        pin
        mode
        pull
        callback
        """

        _check_pin_availability(pin)
        self.pin = pin

        self.mode = mode
        self.pull = pull
        self.callback = callback

        self.intrerupt = True

    def disable(self):
        """Disable the interrupt associated with the ExtInt object.

        This could be useful for debouncing."""
        self.intrerupt = False

    def enable(self):
        """Enable a disabled interrupt."""
        self.intrerupt = True

    def line(self):
        raise NotImplementedError()

    def swint(self):
        raise NotImplementedError()


class Accel:

    @property
    def x(self):
        return randint(0, 10)

    @property
    def y(self):
        # sys.stderr.write("ACCEL: y\n")
        return randint(0, 10)


class LCD:

    def __init__(self, lcd):
        """

        Parameters
        ----------
        lcd
        """
        self._y = lcd['y']
        self._x = lcd['x']
        self.skin_position = None
        self._buffer = None
        self._hidden_buffer = {}

        self.backlight = None
        self.contrast_value = None

    def __call__(self, skin_position):
        self.skin_position = skin_position
        if skin_position == 'Y':
            self._x, self._y = self._y, self._x
        self.fill(0)

        return self

    def command(self, instr_data, buf):
        """Send an arbitrary command to the LCD. Pass 0 for instr_data to send
        an instruction, otherwise pass 1 to send data. buf is a buffer
        with the instructions/data to send.

        """
        # sys.stderr.write("LCD:command: %s %s\n" % (instr_data, buf))
        raise NotImplementedError()

    def contrast(self, value):
        # sys.stderr.write("LCD:contrast: %s\n" % value)
        self.contrast_value = value

    def get(self, x, y):
        # sys.stderr.write("LCD:get: %sx%s\n" % (x, y))
        if self._buffer is None:
            return False
        return self._buffer[(x, y)]

    def light(self, value):
        # sys.stderr.write("LCD:light: %s\n" % value)
        self.backlight = bool(value)

    def fill(self, colour):
        # sys.stderr.write("LCD:fill: %s\n" % colour)
        for y in range(self._y):
            for x in range(self._x):
                self.pixel(x, y, colour)

    def pixel(self, x, y, colour):
        # sys.stderr.write("LCD:fill: %sx%s %s\n" % (x, y, colour))
        self._hidden_buffer[(x, y)] = colour

    def show(self):
        # sys.stderr.write("LCD:show\n")
        self._buffer = self._hidden_buffer.copy()

    def text(self, text, x, y, colour):
        # sys.stderr.write("LCD:text %s %sx%s %s\n" % (text, x, y, colour))
        # font = 'clr8x8'
        # figlet = Figlet(font=font, width=self._x)
        # txt = figlet.renderText(text)
        txt = text
        dx = 0
        dy = 0
        color = 0
        for item in txt:
            if item == ' ':
                color = int(not bool(colour))
            elif item == '#':
                color = colour
            elif item == '\n':
                dy += 1
                dx = 0
                continue
            self.pixel(dx + x, dy + y, color)
            dx += 1

    def write(self, text):
        # sys.stderr.write("LCD:write: %s\n" % text)
        self.text(text, 0, 0, 0)
        self.show()

    def _print_hidden_buffer(self):
        for y in range(self._y):
            for x in range(self._x):
                sys.stdout.write(str(self._hidden_buffer[(x, y)]))
            sys.stdout.write('\n')


class LED:

    # Values in percentage
    _intensity_min = 0
    _intensity_max = 100

    def __init__(self, color):
        self._intensity = 0
        self._color = color

    def on(self):
        sys.stderr.write("LED %s: on\n" % self._color)
        self._intensity = self._intensity_max

    def off(self):
        sys.stderr.write("LED %s: off\n" % self._color)
        self._intensity = self._intensity_min

    def toggle(self):
        sys.stderr.write("LED %s: toggle\n" % self._color)
        if self._intensity == self._intensity_min:
            return self.on()
        return self.off()

    def intensity(self, value=None):
        sys.stderr.write("LED %s: intensity %d\n" % (self._color, value))
        if value is None:
            return self._intensity

        self._intensity = value


class Switch:
    """A Switch object is used to control a push-button switch.

    http://docs.micropython.org/en/latest/library/pyb.Switch.html
    """

    _pressed = False

    def __init__(self, name=None, callable_func=None):
        self._name = name
        self._callable = callable_func

    def __call__(self):
        sys.stderr.write(
            "SWITCH {} call > {}:\n".format(self._name, self._pressed)
        )
        return self._pressed

    def callback(self, callable_func):
        sys.stderr.write(
            "SWITCH {}: callback {}\n".format(self._name, callable_func)
        )
        self._callable = callable_func

    def press(self):
        sys.stderr.write("SWITCH {}: pressed\n".format(self._name))
        self._pressed = True

    def release(self):
        sys.stderr.write("SWITCH {}: released\n".format(self._name))
        self._pressed = False

    def update(self):
        if self._pressed and self._callable is not None:
            self._callable()


class ADC:
    """Create an ADC object associated with the given pin.

    This allows you to then read analog values on that pin.

    http://docs.micropython.org/en/latest/library/pyb.ADC.html"""

    def __init__(self, pin):
        _check_pin_availability(pin)
        self._pin = pin

        self._value = randint(0, 4095)

    def read(self):
        """Read the value on the analog pin and return it

        Returns
        -------
        out : int
            Value between 0 and 4095
        """

        return self._value

    def read_timed(self, buf, timer):
        """Read analog values into buf at a rate set by the timer object.

        Parameters
        ----------
        buf: ArrayType
            The ADC values have 12-bit resolution and are stored directly
            into buf if its element size is 16 bits or greater.

            If buf has only 8-bit elements (eg a bytearray) then the
            sample resolution will be reduced to 8 bits.
        timer: Timer
            A sample is read each time the timer triggers. T
            he timer must already be initialised and running at the
            desired sampling frequency.

        Returns
        -------

        """
        _timer = timer
        for j in range(len(buf)):
            buf[j] = randint(0, 1)

        return buf


class ADCAll:
    """http://docs.micropython.org/en/latest/library/pyb.ADC.html"""

    def __init__(self, resolution):

        self.resolution = resolution

        raise NotImplementedError()


class CAN:
    """http://docs.micropython.org/en/latest/library/pyb.CAN.html"""
    def __init__(self, bus):
        self.bus = bus
        raise NotImplementedError()


class DAC:
    """The DAC is used to output analog values (voltage) on pin X5 or pin X6.


    The output voltage will be between 0 and 3.3V

    Pyboard documentation:
        http://docs.micropython.org/en/latest/library/pyb.DAC.html"""

    NORMAL = 1
    CIRCULAR = 2

    def __init__(self, port, bits=8, buffering=None):
        """Construct a new DAC object.

        When buffering is enabled the DAC pin can drive loads down to 5KΩ.
        Otherwise it has an output impedance of 15KΩ maximum: consequently to
        achieve a 1% accuracy without buffering requires the applied load to be
        less than 1.5MΩ. Using the buffer incurs a penalty in accuracy,
        especially near the extremes of range.

        Parameters
        ----------
        port: Pin or int
            Pin object
            OR
            An integer (1 or 2). DAC(1) is on pin X5 and DAC(2) is on pin X6.
        bits: int
            Resolution, and can be 8 or 12.
            The maximum value for the write and write_timed methods will
             be 2**``bits``-1.
        buffering: bool, optional
            Selects the behaviour of the DAC op-amp output buffer, whose
            purpose is to reduce the output impedance.
            If:
                None
                    It selects the default (buffering enabled for
                    DAC.noise(), DAC.triangle() and DAC.write_timed(), and
                    disabled for DAC.write()),
                False:
                    Disable buffering completely
                True:
                    Enable output buffering.
            Defaults to None.
        """

        # Check port input validity
        if type(port) == int:
            if port == 1:
                pin_name = 'X5'
            elif port == 2:
                pin_name = 'X6'
            else:
                raise Exception("Allocated Pin cannot be used for DAC.")
        elif isinstance(port, Pin):
            pin_name = port.name
        else:
            raise Exception("Allocated Pin is not of valid type.")

        _check_pin_availability(pin_name)
        self.port = port

        # Check bits input validity
        if type(bits) != int:
            raise Exception("Input bits is of not int type.")
        if bits not in [8, 12]:
            raise Exception("Input bits has to be either 8 or 12.")

        self.bits = bits
        self.buffering = buffering

        # Values defined in subsequent methods
        self.value = None

    def init(self):
        raise NotImplementedError()

    def deinit(self):
        """De-initialise the DAC making its pin available for other uses."""
        raise NotImplementedError()

    def noise(self, freq):
        """Generate a pseudo-random noise signal.

        A new random sample is written to the DAC output at the given frequency."""
        raise NotImplementedError()

    def triangle(self, freq):
        """Generate a triangle wave.

        The value on the DAC output changes at the given frequency, and the frequency of the repeating triangle wave itself is 2048 times smaller."""
        raise NotImplementedError()

    def write(self, value):
        """Direct access to the DAC output.

        Parameters
        ----------
        value: int
            The minimum value is 0.
            The maximum value is 2**``bits``-1, where bits is set when creating the DAC object or by using the init method.
        """
        if type(value) != int:
            raise Exception('DAC value must be an integer.')

        if value < 0:
            raise Exception('DAC Value has to be positive.')
        elif value > 2 ** self.bits -1:
            raise Exception('Given value is too large.')

        self.value = value

    def write_timed(self, data, freq, mode=NORMAL):
        """Initiates a burst of RAM to DAC using a DMA transfer.

        Parameters
        ----------
        data: bytearray
            Treated as an array of bytes in 8-bit mode, and an array of
            unsigned half-words (array typecode ‘H’) in 12-bit mode.
        freq: int, Timer
            An integer specifying the frequency to write the DAC
            samples at, using Timer(6).
            OR
            An already-initialised Timer object which is used to trigger
            the DAC sample. Valid timers are 2, 4, 5, 6, 7 and 8.
        mode: NORMAL or CIRCULAR
        """
        data = bytes([self.bits])

        self.value = data
        raise NotImplementedError()


class I2C:
    """http://docs.micropython.org/en/latest/library/pyb.I2C.html"""

    MASTER = 0
    SLAVE = 1

    def __init__(self, bus, *args):
        self._bus = bus

        # Pyboard connections
        if bus == 1:
            self._scl_pin_number = 'X9'
            self._sda_pin_number = 'X10'
        elif bus == 2:
            self._scl_pin_number = 'Y9'
            self._sda_pin_number = 'Y10'

        self._scl_pin = Pin(self._scl_pin_number)
        self._sda_pin = Pin(self._sda_pin_number)

        # Parameters
        self._mode = None
        self._addr = None
        self._baudrate = None
        self._gencall = None
        self._dma = None

    def deinit(self):
        """Turn off the I2C bus."""
        raise NotImplementedError()

    def init(self, mode, addr=0x12, baudrate=400000, gencall=False, dma=False):
        """

        Parameters
        ----------
        mode: str
            Must be either I2C.MASTER or I2C.SLAVE
        addr: str
            Only sensible for a slave.
            Optional, defaults to 0x12.
        baudrate: int
            SCL clock rate (only sensible for a master)
            Optional, defaults to 400000.
        gencall: bool
            Whether to support general call mode.
            Optional, defaults to False.
        dma: bool
            Whether to allow the use of DMA for the I2C transfers
            (note that DMA transfers have more precise timing but
            currently do not handle bus errors properly)
        """
        if self._mode in [self.MASTER, self.SLAVE]:
            self._mode = mode
        else:
            raise AttributeError('Must be either MASTER or Slave')

        self._addr = addr
        self._baudrate = baudrate
        self._gencall = gencall
        self._dma = dma

    def is_ready(self, addr):
        """Check if an I2C device responds to the given address.

        Only valid when in master mode.

        Parameters
        ----------
        addr : str
            I2C address (in hexadecimal) to be investigated.

        Returns
        -------
        out: bool
            True, if an I2C device responds to the given address.
            False, otherwise
        """

    def mem_read(self, data, addr, memaddr, timeout=5000, addr_size=8):
        raise NotImplementedError()

    def mem_write(self, data, addr, memaddr, timeout=5000, addr_size=8):
        raise NotImplementedError()

    def recv(self, recv, addr=0x00, timeout=5000):
        """

        Parameters
        ----------
        recv: int, bytearray
            Can be:
                an integer, which is the number of bytes to receive
                a mutable buffer, which will be filled with received bytes
        addr: str
            The address to receive from (only required in master mode)
        timeout: int
             Timeout in milliseconds to wait for the receive.

        Returns
        -------
        out : int, bytearray
            If recv is an integer then a new buffer of the bytes received.
            Otherwise, the same buffer that was passed in to recv.
        """

        if type(recv) is int:
            out = bytes(recv)
        elif type(recv) is bytearray:
            out = recv
        else:
            raise TypeError('Argument should be of type int or bytearray.')

        if self.is_ready(addr):
            raise OSError('Address not active.')

        return out

    def send(self, send, addr=0x00, timeout=5000):
        """

        Parameters
        ----------
        send: int, bytearray
            Data to send (an integer to send, or a buffer object)
        addr: bytearray
            The address to send to (only required in master mode)
        timeout: int
             Timeout in milliseconds to wait for the receive.
        """
        if type(send) not in [int, bytearray]:
            raise TypeError('Argument should be of type int or bytearray.')
        if addr is not self._addr:
            raise Exception("Address is not active.")

    def scan(self):
        """Scan all I2C addresses and return active ones.

        Scans addressed from 0x01 to 0x7f.
        Only valid when in master mode.

        Returns
        -------
        out : list
            List of I2C addresses that respond
        """
        active_addresses = []

        inspected_addresses_list = range(1, 128)
        for integer in inspected_addresses_list:
            address = hex(integer)
            if self.is_ready(address):
                active_addresses.append(address)

        return active_addresses


class PinAF:
    """http://docs.micropython.org/en/latest/library/pyb.I2C.html"""
    def __init__(self, bus):

        self.bus = bus
        raise NotImplementedError()


# http://docs.micropython.org/en/latest/library/pyb.Pin.html#class-pinaf-pin-alternate-functions

class RTC:
    """http://docs.micropython.org/en/latest/library/pyb.RTC.html"""
    def __init__(self):
        raise NotImplementedError()


class Servo:
    """http://docs.micropython.org/en/latest/library/pyb.Servo.html"""
    def __init__(self, identifier):
        self.id = identifier
        raise NotImplementedError()


class SPI:
    """http://docs.micropython.org/en/latest/library/pyb.SPI.html"""

    # ToDO: finish

    MASTER = 0
    SLAVE = 1
    LSB = 2
    MSB = 3

    def __init__(self, bus, mode, **kwargs):

        self.bus = bus
        self.mode = mode

        self._sent_data = None
        self._out_data = None

        if kwargs:
            self.init(kwargs)

    def deinit(self):
        raise NotImplementedError()

    def init(self, kwargs):
        raise NotImplementedError()

    def send(self, data, timeout=5000):
        """Send data on the bus,

        Parameters
        ----------
        data: int, bytes or bytearray
            Data to send
        timeout: int
            Milliseconds to wait for the send.
        """
        _timeout = timeout
        self._sent_data = data

    def recv(self, recv, timeout=5000):
        """Receive data on the bus.

        Parameters
        ----------
        recv: int or buffer
            If  int, number of bytes to receive
                a mutable buffer, which will be filled with received bytes.
        timeout: int
            Milliseconds to wait for the receive.

        Returns
        -------
        out: int or buffer
            If recv:
                is an integer then a new buffer of the bytes received,
                otherwise the same buffer that was passed in to recv.
        """
        if type(recv) == int:
            self._out_data = []
            for j in range(recv):
                self._out_data.append(randint(0, 1))
        else:
            address = randint(0, 255)
            self._out_data = bytes([address, 0])

        return self._out_data

    def send_recv(self, send, recv=None, timeout=5000):
        """Send and receive data on the bus at the same time:

        Parameters
        ----------
        send: int, buffer
            Data to send
        recv: buffer
            Mutable buffer which will be filled with received bytes.
            It can be the same as send, or omitted.
            If omitted, a new buffer will be created.
        timeout: int
            Milliseconds to wait for the receive.

        Returns
        -------
        out : buffer
            Received bytes.
        """

        self.send(send)
        _timeout = timeout

        if recv:
            for j in range(len(recv)):
                recv[j] = randint(0, 1)
        else:
            address = randint(0, 255)
            self._out_data = bytes([address, 0])

        return self._out_data


class Timer:
    """

    http://docs.micropython.org/en/latest/library/pyb.Timer.html"""

    PWM = Mock()
    PWM_INVERTED = Mock()
    OC_TIMING = Mock()
    OC_CTIVE = Mock()
    OC_INACTIVE = Mock()
    OC_TOGGLE = Mock()
    OC_FORCE_ACTIVE = Mock()
    OF_FORCED_INACTIVE = Mock()
    I2C = Mock()
    ENC_A = Mock()
    ENC_B = Mock()
    ENC_AB = Mock()

    def __init__(self, pin_id, freq=100, prescaler=83, period=999):
        """Construct a new timer object of the given id."""
        self._id = pin_id

        self.timer_frequency = freq
        self.timer_prescaler = prescaler
        self.timer_period = period

        self.counter = None

    def init(self):
        raise NotImplementedError()

    def deinit(self):
        raise NotImplementedError()

    def callback(self):
        raise NotImplementedError()

    @staticmethod
    def channel(channel, mode, **kwargs):
        return TimerChannel(channel, mode, **kwargs)

    def counter(self, value=None):
        """Get or set the timer counter.

        Parameters
        ----------
        value: int, optional
            Defaults to None.

        Returns
        -------
        out: int
        """
        if value is not None:
            self.counter = value
        else:
            return self.counter

    def freq(self, value=None):
        """Get or set the frequency for the timer.

        # Todo:
        Changes prescaler and period if set.

        Parameters
        ----------
        value: int, optional
            Defaults to None.

        Returns
        -------
        out: int
        """
        if value is not None:
            self.timer_frequency = value
        else:
            return self.timer_frequency

    def period(self, value=None):
        """Get or set the period of the timer.

        Parameters
        ----------
        value: int, optional
            Defaults to None.

        Returns
        -------
        out: int
        """
        if value is not None:
            self.timer_period = value
        else:
            return self.timer_period

    def prescaler(self, value=None):
        """Get or set the period of the timer.

        Parameters
        ----------
        value: int, optional
            Defaults to None.

        Returns
        -------
        out: int
        """
        if value is not None:
            self.timer_prescaler = value
        else:
            return self.timer_prescaler

    def source_freq(self):
        """Get the frequency of the source of the timer.

        Returns
        -------
        out: int
        """
        return self.timer_frequency


class TimerChannel:

    def __init__(self, channel, mode, **kwargs):
        # Todo: finish
        self.value = None
        self.channel = channel
        self.mode = mode

        if kwargs:
            pass

    def capture(self):
        raise NotImplementedError()

    def compare(self):
        raise NotImplementedError()

    def pulse_width(self):
        raise NotImplementedError()

    def pulse_width_percent(self, percent=None):
        """Get or set the pulse width percentage associated with a channel.

        The value can be an integer or floating-point number for more accuracy.

        Parameters
        ----------
        percent : float, optional
            The value is a number between 0 and 100 and sets the percentage of
            the timer period for which the pulse is active.
            For example, a value of 25 gives a duty cycle of 25%.
            If not given, defaults to None.

        Returns
        -------
        out : float
            The current value of the timer channel.
        """

        if percent is None:
            return self.value

        self.value = percent


class UART:
    """http://docs.micropython.org/en/latest/library/pyb.UART.html"""

    RTS = 1
    CTS = ""

    def __init__(self, bus, baudrate, **kwargs):

        self.bus = bus
        self.baudrate = baudrate

        if kwargs:
            self.init(kwargs)

        self._read_buf = None
        self._written_buf = None

    def init(self, kwargs):
        raise NotImplementedError()

    def deinit(self):
        raise NotImplementedError()

    def any(self):
        """Returns the number of bytes waiting (may be 0)."""
        return randint(0, 10)

    def read(self, nbytes=None):
        """Read characters.

        If nbytes is specified, read at most that many bytes.
            If nbytes are available in the buffer, returns immediately,
            otherwise returns when sufficient characters arrive or the
            timeout elapses.

        If nbytes is not given, the method reads as much data as possible.
            It returns after the timeout has elapsed.

        Note:
            for 9 bit characters each character takes two bytes, nbytes
            must be even, and the number of characters is nbytes/2.

        Return value: a bytes object containing the bytes read in.
        Returns None on timeout."""

        if nbytes:
            number_of_bytes = nbytes
        else:
            number_of_bytes = 5

        self._read_buf = bytes(number_of_bytes)

        return self._read_buf

    def readchar(self):
        raise NotImplementedError()

    def readinto(self):
        raise NotImplementedError()

    def readline(self):
        raise NotImplementedError()

    def write(self, buf):
        """Write the buffer of bytes to the bus.

        If characters are 7 or 8 bits wide then each byte is one
        character. If characters are 9 bits wide then two bytes are used
        for each character (little endian), and buf must contain an even
        number of bytes.

        Parameters
        ----------
        buf: buffer

        Returns
        -------
        out : int
            number of bytes written.
            If a timeout occurs and no bytes were written returns
        """

        # Todo: implement a timeout condition.
        timeout = False

        while not timeout:
            self._written_buf = buf
            out = len(self._written_buf)
            return out

    def writechar(self, char):
        """Write a single character on the bus.

        Parameters
        ----------
        char: int

        Returns
        -------
        out: None.
            See note below if CTS flow control is used.
        """
        self._written_buf += char

    def sendbreak(self):
        raise NotImplementedError()


class USB_VCP:
    """http://docs.micropython.org/en/latest/library/pyb.USB_VCP.html"""
    def __init__(self):
        raise NotImplementedError()


#
# Time related functions
#

def delay(milliseconds):
    sys.stderr.write("PYB: delay %s\n" % milliseconds)
    sleep(milliseconds / 1000)


def udelay(us):
    sys.stderr.write("PYB: udelay %s\n" % us)
    sleep(us / 1000000)


# def millis():
#     sys.stderr.write("PYB: millis\n")
#     result = micros() / 1000
#     return result


# def micros():
#     sys.stderr.write("PYB: micros\n")
#     delta = datetime.now() - _board.boot_time
#     result = delta.total_seconds() * 1000000
#     return result


# def elapsed_millis(start):
#     sys.stderr.write("PYB: elapsed_millis\n")
#     result = elapsed_micros(start) / 1000
#     return result


# def elapsed_micros(start):
#     sys.stderr.write("PYB: elapsed_micros\n")
#     result = micros() - start
#     return result


# def hard_reset():
#     """Resets the pyboard in a manner similar to pushing the external
#     RESET button.
#     """
#     _board.boot()


def bootloader():
    """Activate the bootloader without BOOT\* pins."""
    raise NotImplementedError()


def disable_irq():
    """Disable interrupt requests.
    Returns the previous IRQ state: ``False``/``True`` for
    disabled/enabled IRQs respectively.  This return value can be
    passed to enable_irq to restore the IRQ to its original state.
    """
    raise NotImplementedError()


def enable_irq(state=True):
    """Enable interrupt requests.
    If ``state`` is ``True`` (the default value) then IRQs are
    enabled.  If ``state`` is ``False`` then IRQs are disabled.  The
    most common use of this function is to pass it the value returned
    by ``disable_irq`` to exit a critical section.
    """
    raise NotImplementedError()


def freq(sysclk=None, hclk=None, pclk1=None, pclk2=None):
    """If given no arguments, returns a tuple of clock frequencies:
    (sysclk, hclk, pclk1, pclk2).
    These correspond to:

        - sysclk: frequency of the CPU
        - hclk: frequency of the AHB bus, core memory and DMA
        - pclk1: frequency of the APB1 bus
        - pclk2: frequency of the APB2 bus

    If given any arguments then the function sets the frequency of the
    CPU, and the busses if additional arguments are given.
    Frequencies are given in Hz.  Eg freq(120000000) sets sysclk (the
    CPU frequency) to 120MHz.  Note that not all values are supported
    and the largest supported frequency not greater than the given
    value will be selected.

    Supported sysclk frequencies are (in MHz): 8, 16, 24, 30, 32, 36,
    40, 42, 48, 54, 56, 60, 64, 72, 84, 96, 108, 120, 144, 168.

    The maximum frequency of hclk is 168MHz, of pclk1 is 42MHz, and of
    pclk2 is 84MHz.  Be sure not to set frequencies above these
    values.

    The hclk, pclk1 and pclk2 frequencies are derived from the sysclk
    frequency using a prescaler (divider).  Supported prescalers for
    hclk are: 1, 2, 4, 8, 16, 64, 128, 256, 512.  Supported prescalers
    for pclk1 and pclk2 are: 1, 2, 4, 8.  A prescaler will be chosen
    to best match the requested frequency.

    A sysclk frequency of 8MHz uses the HSE (external crystal)
    directly and 16MHz uses the HSI (internal oscillator) directly.
    The higher frequencies use the HSE to drive the PLL (phase locked
    loop), and then use the output of the PLL.

    Note that if you change the frequency while the USB is enabled
    then the USB may become unreliable.  It is best to change the
    frequency in boot.py, before the USB peripheral is started.  Also
    note that sysclk frequencies below 36MHz do not allow the USB to
    function correctly.
    """
    raise NotImplementedError()


def wfi():
    """Wait for an internal or external interrupt.

    This executes a ``wfi`` instruction which reduces power
    consumption of the MCU until any interrupt occurs (be it internal
    or external), at which point execution continues.  Note that the
    system-tick interrupt occurs once every millisecond (1000Hz) so
    this function will block for at most 1ms.
    """
    raise NotImplementedError()


def stop():
    """Put the pyboard in a "sleeping" state.

    This reduces power consumption to less than 500 uA.  To wake from
    this sleep state requires an external interrupt or a
    real-time-clock event.  Upon waking execution continues where it
    left off.

    See :meth:`rtc.wakeup` to configure a real-time-clock wakeup
    event.
    """
    raise NotImplementedError()


def standby():
    """Put the pyboard into a "deep sleep" state.

    This reduces power consumption to less than 50 uA.  To wake from
    this sleep state requires a real-time-clock event, or an external
    interrupt on X1 (PA0=WKUP) or X18 (PC13=TAMP1).  Upon waking the
    system undergoes a hard reset.

    See :meth:`rtc.wakeup` to configure a real-time-clock wakeup
    event.
    """
    raise NotImplementedError()


def have_cdc():
    """Return True if USB is connected as a serial device, False otherwise.

    This function is deprecated.  Use pyb.USB_VCP().isconnected()
    instead.
    """
    raise NotImplementedError()


def hid(buttons, x, y, z):
    """Takes a 4-tuple (or list) and sends it to the USB host (the PC) to
    signal a HID mouse-motion event.

    This function is deprecated.  Use pyb.USB_HID().send(...) instead.
    """
    raise NotImplementedError()


def info(dump_alloc_table=None):
    """Print out lots of information about the board."""
    raise NotImplementedError()


def main(filename):
    """Set the filename of the main script to run after boot.py is
    finished.  If this function is not called then the default file
    main.py will be executed.

    It only makes sense to call this function from within boot.py.
    """
    raise NotImplementedError()


def mount(device, mountpoint, *args, readonly=False, mkfs=False):
    """Mount a block device and make it available as part of the
    filesystem.  ``device`` must be an object that provides the block
    protocol:

    - ``readblocks(self, blocknum, buf)``
    - ``writeblocks(self, blocknum, buf)`` (optional)
    - ``count(self)``
    - ``sync(self)`` (optional)

    ``readblocks`` and ``writeblocks`` should copy data between
    ``buf`` and the block device, starting from block number
    ``blocknum`` on the device.  ``buf`` will be a bytearray with
    length a multiple of 512.  If ``writeblocks`` is not defined
    then the device is mounted read-only.  The return value of
    these two functions is ignored.

    ``count`` should return the number of blocks available on the
    device.
    ``sync``, if implemented, should sync the data on the device.

    The parameter ``mountpoint`` is the location in the root of the
    filesystem to mount the device.  It must begin with a
    forward-slash.

    If ``readonly`` is ``True``, then the device is mounted read-only,
    otherwise it is mounted read-write.

    If ``mkfs`` is ``True``, then a new filesystem is created if one
    does not already exist.

    To unmount a device, pass ``None`` as the device and the mount
    location as ``mountpoint``.
    """
    raise NotImplementedError()


def repl_uart(uart):
    """Get or set the UART object where the REPL is repeated on."""
    raise NotImplementedError()


def rng():
    """Return a 30-bit hardware generated random number."""
    raise NotImplementedError()


def sync():
    """Sync all file systems."""
    raise NotImplementedError()


def unique_id():
    """Returns a string of 12 bytes (96 bits), which is the unique ID of
    the MCU.
    """
    raise NotImplementedError()

