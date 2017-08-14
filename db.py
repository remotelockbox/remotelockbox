
import shelve
from os import path

from werkzeug import generate_password_hash, check_password_hash

import hardware

class LockState:
    def __init__(self):
        self.solenoid = hardware.SolenoidSwitch()
        self.last_locked_by = None

    def lock(self, user_id):
        self.solenoid.open()
        self.last_locked_by = user_id

    def unlock(self, user_id):
        self.solenoid.close()
        self.last_locked_by = user_id
    
    def is_locked(self):
        return not self.solenoid.is_closed()

    def sync(self):
        """ re-apply solenoid state in case the hardware was
            out of sync with the software.
        """
        if self.solenoid.closed:
            self.solenoid.close()
        else:
            self.solenoid.open()

class User:
    def __init__(self, id, pin=None):
        self.id = id
        if pin:
            self.set_pin(pin)

    def set_pin(self, pin):
        self.pin_hash = generate_password_hash(pin)

    def check_pin(self, pin):
        return check_password_hash(self.pin_hash, pin)

def get_user(id):
    for user in users:
        if id == user.id:
            return user

# Open database
db = shelve.open('lock-settings.db', writeback=True)

# Populate database if it is empty
db.setdefault('lock_state', LockState())
db.setdefault('users', [User('primary', '1234'), User('sub', '0000')])

lock_state = db['lock_state']
users = db['users']
