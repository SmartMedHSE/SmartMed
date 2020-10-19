from abc import ABC, abstractmethod

import time

import dash
import webbrowser

# logging decorator
import sys
sys.path.append("..")
from logs.logger import debug


class Dashboard(ABC):
	'''Dashboard Interface'''

	def __init__(self):
		external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
		external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']
		self.app = dash.Dash(
			server=True, external_stylesheets=external_stylesheets, external_scripts=external_scripts)

	@debug
	@abstractmethod
	def _generate_layout(self):
		raise NotImplementedError

	@debug
	def start(self, debug=False):
		self.app.layout = self._generate_layout()
		webbrowser.open("http://127.0.0.1:8050/")
		self.app.run_server(debug=debug)
