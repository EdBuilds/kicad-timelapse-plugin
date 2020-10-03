from threading import Timer
import time

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.start()

    def _run(self):
        # Function returns if timer should repeat or not.
        repeat = self.function(*self.args, **self.kwargs)
        if repeat:
            self.start()

    def start(self):
        self._timer = Timer(self.interval, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()