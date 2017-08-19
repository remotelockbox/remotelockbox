from wtforms import *

class ScheduleForm(Form):
    unlock_date = StringField('Unlock on Date')
