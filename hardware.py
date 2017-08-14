import time

class SolenoidSwitch:
    def __init__(self, closed=True):
        self.closed = closed
        self.last_open = 0

    def open(self):
        print("solenoid opened")
        if self.closed:
            self.last_open = time.time()
        self.closed = False

    def close(self):
        print("solenoid closed")
        self.closed = True;
    
    def is_closed(self):
        return self.closed
