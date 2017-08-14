
import shelve
from os import path

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

SHELVE_DB = 'lock-settings.db'

db = shelve.open(SHELVE_DB, writeback=True)

db.setdefault('lock_state', LockState())

lock_state = db['lock_state']
