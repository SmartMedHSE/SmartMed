import requests
from flask import Flask, request, abort
import sys
import threading
sys.path.append('C:\\Users\\egorl\\Desktop\\SmartMed-1')
from SmartMedApp.backend.ModuleManipulator import ModuleManipulator

app = Flask(__name__)




@app.route('/api/descriptive', methods=['POST'])
def requesting():
    if request.method == 'POST':
        data_json = request.json
        data_json['MODULE_SETTINGS']['data']['path'] = 'C:\\Users\\egorl\\Desktop\\Глаукому.xlsx'
        print(data_json)    
        module_starter = ModuleManipulator(data_json)
        threading.Thread(target=module_starter.start, daemon=True).start()
    return 'get'




if __name__ == '__main__':
   app.run(host='127.0.0.1', port=13000, debug=True)