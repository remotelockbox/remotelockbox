from wtforms import *


class ScheduleForm(Form):
    unlock_date = DateTimeField('Unlock on Date', format='%Y-%m-%d %H:%M')
