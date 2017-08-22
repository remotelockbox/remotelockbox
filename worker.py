from datetime import datetime
import logging
import threading
import werkzeug.serving
from db import db, lock_state

timer = None

def start():
    global timer
    if not werkzeug.serving.is_running_from_reloader():
        timer = threading.Timer(5, _run)
        timer.start()

def stop():
    if timer:
        timer.cancel()
        check_expired()

def _run():
    check_expired()
    start()

def check_expired():
    if 'schedule_form' in db and 'unlock_date' in db['schedule_form']:
        print("expired")
        unlock_time = datetime.strptime(db['schedule_form']['unlock_date'], '%Y-%m-%d %H:%M')
        if unlock_time <= datetime.now():
            logging.info("scheduled unlock (#s)".format(unlock_time))
            lock_state.unlock(db['schedule_user_id'])
            del db['schedule_form']
            del db['schedule_user_id']
            db.sync()

