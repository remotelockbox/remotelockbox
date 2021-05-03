from datetime import datetime
import logging
import threading
import werkzeug.serving
import db

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
    if db.schedule_form and 'unlock_date' in db.schedule_form:
        unlock_time = datetime.strptime(db.schedule_form['unlock_date'], '%Y-%m-%d %H:%M')
        if unlock_time <= datetime.now():
            logging.info("scheduled unlock (#s)".format(unlock_time))
            db.lock_state.unlock(db.schedule_user_id)
            db.schedule_form = None
            db.schedule_user_id = None
            db.save()
