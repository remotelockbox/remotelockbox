# Remote Lock Box

A web-server that controls an electronic lockbox.
It is meant to be installed securely on an embedded computer inside the box.

# Running

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

# Development

During development, run the `./debug` script to start in debug mode. The server
will automatically restart when files change.


