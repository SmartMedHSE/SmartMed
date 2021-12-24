import webbrowser
import random
import socket
from contextlib import closing
from abc import ABC, abstractmethod

import dash
from logs.logger import debug


class Dashboard(ABC):
    '''

    Dashboard Interface

    Each ConcreteDashboar inreases port number 
    and Dashboar_i is opened on localhost with port = 8000 + i
    in daemon thread

    '''
    # Create random port
    port = random.randint(8000, 49151)

    @debug
    def __init__(self):
        # include general styleshits and scripts
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        external_scripts = [
            'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']

        # create Dash(Flask) server
        self.app = dash.Dash(
            server=True, external_stylesheets=external_stylesheets, external_scripts=external_scripts)


    @debug
    @abstractmethod
    def _generate_layout(self):
        '''
        abstractmethod to generate dashboard layout
        '''
        raise NotImplementedError

    @debug
    def check_socket(self):
        while(True):
            # Searchig for available port
            with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
                if sock.connect_ex(('127.0.0.1', self.port)) == 0:
                    self.port = random.randint(8000, 49151) # Port isn't available, choosing the next one
                else:
                    return self.port # Port is available


    @debug
    def start(self, debug=False):
        # generate layout
        self.app.layout = self._generate_layout()

        # set port
        port = self.check_socket()
        # open dashboard
        webbrowser.open(f"http://127.0.0.1:{port}/")

        # run dashboard
        self.app.run_server(debug=debug, port=port)
