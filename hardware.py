import logging
import os
import time

# When SIMULATE_HARDWARE is set, don't really do hardware IO
use_gpio = 'SIMULATE_HARDWARE' not in os.environ

# Set whether the relay is Normally Closed (NC) or Normally Open (NO)
# Normally Open is more secure but leaves the box locked when the Pi loses power (or if it crashes!).
# This is OK if someone has access to the override key for the safe. That key will still work.
#
# Normally Closed will let you operate the safe when the Pi loses power. If your Pi is powered
# externally, this means that simply unplugging the safe from the wall will let you unlock it
# using the combination. This mode may be useful if there is no override key for the safe
# or if the computer is powered by an internal battery.
#
# Read this link for a graphical explanation: http://www.pcbheaven.com/wikipages/How_Relays_Work
#
# This setting MUST match the wiring of your relay.
# Otherwise the meaning of locked and unlocked will be reversed!
relay_nc=False

relay_pin = 17 # GP17, pin #11

if use_gpio:
    import gpiozero
    _relay = gpiozero.DigitalOutputDevice(relay_pin, active_high=relay_nc)

class SolenoidSwitch:
    def __init__(self, closed=True):
        self.closed = closed

    def open(self):
        logging.debug("solenoid opened")
        if use_gpio:
            _relay.on()
        self.closed = False

    def close(self):
        logging.debug("solenoid closed")
        if use_gpio:
            _relay.off()
        self.closed = True;
    
    def is_closed(self):
        return self.closed

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='directly control lockbox hardware')
    parser.add_argument('command', choices=['open', 'close'])
    args = parser.parse_args()

    switch = SolenoidSwitch()
    if args.command == 'open':
        switch.open()
    elif args.command == 'close':
        switch.close()
    else:
        raise Exception("unknown command")

