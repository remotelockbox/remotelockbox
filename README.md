# Remote Lock Box

A web-server that controls an electronic lockbox.
It is meant to be installed securely on an embedded computer inside the box.

## Running

Install `python3` and `pip3`. On debian, raspbian, or ubuntu,
run `apt install python3 python3-pip`.

Then execute `pip3 install -r requirements.txt` to install libraries
required by this program.

Run the program by executing `./run`.

A database called `lock-settings.db` will be created in the current directory.

The lock box supports up to two users. The primary user has full control
of the box at all times. The secondary user (the 'sub' user), can control
the box only when the primary user has unlocked the box. The sub can
lock it themselves but cannot unlock it once it has been locked by the
primary account holder.

When first installed, these are the default PINs:

    Primary - 1234
    Sub     - 0000

If you change your PIN and forget it, reset all the settings by
deleting `lock-settings.db`. Depending on how you access the files,
that may require physical access inside the lock box. So be careful!

## Development

During development, run the `./debug` script to start in debug mode. The server
will automatically restart when files change.

## Design

This software is designed to control a relay using GPIO. It is built with
the Raspberry Pi in mind but other hardware will also work.

## Hardware Installation

#### Required Parts

 - A tiny linux-based computer with WiFi such as the Raspberry Pi Zero W
 - power supply or battery power for the computer
 - A relay circuit
 - Electronic security box with a keypad that can be removed from the inside.

All of these parts can be acquired for under 100 USD.

You may also need miscellaneous items for interacting with the computer during
setup (keyboard, monitor, sd-card reader, etc.).

Purchase or build a relay circuit.
There is an inexpensive kit that requires assembly and soldering at [Sparkfun](https://www.sparkfun.com/products/13815).

Search for a "Digital Electronic Safe Box" on Amazon or Ebay. You will notice that most of them have the same controls on the front. You want any one of these.

#### Installation Steps

Set a very short and simple PIN on the keypad. Since the keypad only works when this software allows it, you need it to be convenient, not secure.

On the inside of the door, unscrew the panel that contains the electronics and hardware. You need to cut one wire going from the control board to the solenoid that controls the lock.
Connect the relay to each end of the cut wire so the relay is between the solenoid and the control board.

Now connect the relay's 5v control pins to your raspberry pi.

Load this software onto the raspberry pi and run it. Test that it is accessible over your WiFi network (or plug it in via Ethernet if needed).

If your raspberry pi requires wired power, thread the power cable through one of the mounting holes in the back of the case. This may require drilling a wider hole or cutting the connector off your cable and and splicing it back on.

If you use battery power, connect it to its battery. If your safe uses 4 AAA (or AA) batteries, you can even power the raspberry pi from the safe's own batteries. The details on how to do this may vary by manufacture.

You can use the included command line utility to turn the relay on and off.
Sometimes this is useful when troubleshooting. Run the command-line program
with `python3 hardware.py --help` and read the usage instructions.

If you have any bare circuit boards, be sure to insulate them from the metal
box. You can use a small cardboard box or pieces of paper.
