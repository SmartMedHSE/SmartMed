# logging decorator
from logs.logger import debug
from .WrappedStartingWindow import WrappedStartingWindow


class StartingApp():

    @debug
    def __init__(self):
        self.startingWindow = WrappedStartingWindow()

    @debug
    def start(self):
        self.startingWindow.show()
