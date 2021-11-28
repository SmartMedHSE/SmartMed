import os
import sys
import threading

from flask import Flask, request

from backend.ModuleManipulator import ModuleManipulator

BASE_DIR = os.path.abspath(os.curdir)
sys.path.append(BASE_DIR)

app = Flask(__name__)


@app.route('/api/descriptive', methods=['POST'])
def requesting():
    if request.method == 'POST':
        data_json = request.json
        # data_json['MODULE_SETTINGS']['data']['path'] = 'C:\\Users\\egorl\\Desktop\\Глаукому.xlsx'
        module_starter = ModuleManipulator(data_json)
        threading.Thread(target=module_starter.start, daemon=True).start()
    return 'get'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=13000, debug=True)
