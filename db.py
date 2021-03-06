import datetime
import logging
import shelve
import os

from werkzeug.security import generate_password_hash, check_password_hash

import hardware


class LockState:
    def __init__(self):
        self.solenoid = hardware.SolenoidSwitch()
        self.last_locked_by = None
        self.last_locked = datetime.datetime.now()

    def lock(self, user_id):
        if self.solenoid.is_closed():
            self.solenoid.open()
            self.last_locked = datetime.datetime.now()
            self.last_locked_by = user_id
            logging.info('locked by %s', self.last_locked_by)

    def unlock(self, user_id):
        if self.is_locked() and not self.can_unlock(user_id):
            logging.warning('%s could not unlock because it was last locked by %s', user_id, self.last_locked_by)
            return

        self.solenoid.close()
        self.last_locked_by = user_id
        logging.info('unlocked by %s (last locked on %s)', self.last_locked_by, self.last_locked)

    def is_locked(self):
        return not self.solenoid.is_closed()

    def can_unlock(self, user_id):
        return self.last_locked_by == user_id or user_id == 'primary'

    def sync(self):
        """ re-apply solenoid state in case the hardware was
            out of sync with the software.
        """
        if self.solenoid.closed:
            self.solenoid.close()
        else:
            self.solenoid.open()
        logging.info('syncing solenoid state (closed=%s)', self.solenoid.closed)


class User:
    def __init__(self, user_id, pin=None):
        self.id = user_id
        self.pin_hash = None
        if pin:
            self.set_pin(pin)

    def set_pin(self, pin):
        self.pin_hash = generate_password_hash(pin)

    def check_pin(self, pin):
        return check_password_hash(self.pin_hash, pin)


def get_user(user_id):
    for user in users:
        if user_id == user.id:
            return user


lock_state = None
users = []
schedule_form = None
schedule_user_id = None


def _open():
    return shelve.open(os.getenv('LOCK_SETTINGS_PATH', 'lock-settings'), writeback=True)


def read():
    global lock_state, users, schedule_form, schedule_user_id

    with _open() as shelf:
        lock_state = shelf.get('lock_state', LockState())
        users = shelf.get('users', [User('primary', '1234'), User('sub', '0000')])
        schedule_form = shelf.get('schedule_form')
        schedule_user_id = shelf.get('schedule_user_id')


def save():
    with _open() as shelf:
        shelf['lock_state'] = lock_state
        shelf['users'] = users
        shelf['schedule_form'] = schedule_form
        shelf['schedule_user_id'] = schedule_user_id


def clear():
    with _open() as shelf:
        shelf.clear()
