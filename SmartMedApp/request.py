import requests
from flask import Flask, request, abort

#from SmartMedApp.backend.ModuleManipulator import ModuleManipulator

app = Flask(__name__)




@app.route('/api/descriptive', methods=['POST'])
def requesting():
    if request.method == 'POST':
        data_json = request.json
        print(data_json)    
        #ModuleManipulator(data_json).start() 
    return None




if __name__ == '__main__':
   app.run(host='127.0.0.1', port=13000, debug=True)