import webbrowser
from abc import ABC, abstractmethod

import socket

import dash

from logs.logger import debug


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


class Dashboard(ABC):
    """Dashboard Interface"""

    port = 15001
    url_count = 0

    @debug
    def __init__(self):
        # include general styleshits and scripts
        external_stylesheets = [
            'https://codepen.io/chriddyp/pen/bWLwgP.css'
        ]
        external_scripts = [
            'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
        ]

        try:
            settings = self.settings
        except Exception as e:
            print(e)

        try:
            Dashboard.url_count = settings['url_count']
        except Exception as e:
            print(e)

        try:
            self.app = dash.Dash(
                __name__,
                server=settings['server'], url_base_pathname=f"/dash{Dashboard.url_count}/",
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts
            )
        except Exception as e:
            print(e)

    @debug
    @abstractmethod
    def _generate_layout(self):
        '''
        abstractmethod to generate dashboard layout
        '''
        raise NotImplementedError

    @debug
    def start(self, debug=False):
        # generate layout
        self.app.layout = self._generate_layout()

        # open dashboard
        webbrowser.open(f"http://localhost:15001/dash{Dashboard.url_count}/")
