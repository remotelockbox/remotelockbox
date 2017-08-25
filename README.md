# Remote Lock Box

A web-server that controls an electronic lockbox.
It is meant to be installed securely on an embedded computer inside the box.

## Installation

### Setting up your system

Set your time-zone by running `dpkg-reconfigure tzdata`.

#### Raspberry Pi Installation

Use the included `install` script to install this application
and configure it to start on boot. This only works if you
are logged in as the `pi` user.

Check out this repository with git in your home directory and
run the install script:

    git clone https://github.com/remotelockbox/remotelockbox.git
    cd remotelockbox
    bin/install

#### Advanced Manual Installation / Other Linux Distributions

Install `python3` and `pip3`. On debian, raspbian, or ubuntu,
run `apt install python3 python3-pip`.

Execute `pip3 install -r requirements.txt` to install libraries
required by this program.

If you do not want to run as root, allow access to GPIO pins
and make sure your user is a member of the gpio group.

    sudo chown root.gpio /dev/gpiomem
    sudo chmod g+rw /dev/gpiomem

Adapt the included systemd service file to your environment.

### Running the server directly

Normally, you shouldn't have to do this. But if you want to run the server in
your shell without systemd, execute `python3 app.py`. This may be useful when
modifying and testing the program. Run with the `--help` option to see
available command-line options.

A database called `lock-settings.db` will be created in the current directory.

## Using the remotelockbox

Use your web browser to connect to the raspberry pi.

You can find your device's address by running `ip addr`. If your raspberry pi
is wired, usee the `eth0` address. Otherwise, use the address for `wlan0` or
similarly named interface for a wifi connection. Network configuration is not
covered by this document.  Please refer to the Raspberry Pi website for
information about configuring wifi.

The lock box supports up to two users. The primary user has full control
of the box at all times. The secondary user (the 'sub' user), can control
the box only when the primary user has unlocked the box. The sub can
lock it themselves and can set a scheduled unlock but cannot
manually unlock it.

When first installed, these are the default PINs:

    Primary - 1234
    Sub     - 0000

If you change your PIN and forget it, reset all the settings by
deleting `lock-settings.db`. Depending on how you access the files,
that may require physical access inside the lock box. Be careful!

## Development

During development, run the `bin/debug` script to start in debug mode.
The server will automatically restart when files change.

The `debug` script does not operate your hardware by default.

The included test suite simulates requests against the web application
and checks that common usage scenarios work correctly. Run the tests
with `python3 app_test.py`.

## Design

This software is designed to control a relay using GPIO. It is built with
the Raspberry Pi in mind but other hardware will also work.

## Hardware Installation

#### Required Parts

 - A tiny linux-based computer with WiFi such as the Raspberry Pi Zero W
 - Micro-USB power supply
 - A relay circuit
 - Electronic security box with a keypad that can be removed from the inside.

All of these parts can be acquired for under 100 USD.

You may also need miscellaneous items for interacting with the computer during
setup (keyboard, monitor, sd-card reader, etc.).

Purchase or build a relay circuit.
There is an inexpensive kit that requires assembly and soldering at
[Sparkfun](https://www.sparkfun.com/products/13815).

Search for a "Digital Electronic Safe Box" on Amazon or Ebay. You will notice
that most of them have the same controls on the front. You want any one of
these.

#### Installation Steps

Set a very short and simple PIN on the keypad. Since the keypad only works when
this software allows it, you need it to be convenient, not secure.

On the inside of the door, unscrew the panel that contains the electronics and
hardware. You need to cut one wire going from the control board to the solenoid
that controls the lock.

Connect the relay to each end of the cut wire so the relay is between the
solenoid and the control board.

Now connect the relay's 5v control pins to your raspberry pi.

Load this software onto the raspberry pi and run it. Test that it is
accessible over your WiFi network (or plug it in via Ethernet if needed).

Thread the power cable through one of the mounting holes in the back of
the case. This may require drilling a wider hole or cutting the connector
off your cable and and splicing it back on.

You can use the included command line utility to turn the relay on and off.
Sometimes this is useful when troubleshooting. Run the command-line program
with `python3 hardware.py --help` and read the usage instructions.

If you have any bare circuit boards, be sure to insulate them from the metal
box. You can use a small cardboard box or pieces of paper.
