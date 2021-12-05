import os
import sys
import threading

from flask import Flask, request


BASE_DIR = os.path.abspath(os.curdir)
sys.path.append(BASE_DIR)
from backend.ModuleManipulator import ModuleManipulator

app = Flask(__name__)


@app.route('/api/descriptive', methods=['POST'])
def requesting():
    if request.method == 'POST':
        data_json = request.json


    json_example = {
        "MODULE_SETTINGS": 
        {"metrics": 
            {"count": False, "mean": False, "std": False, "max": False, "min": False, "25%": False, 
            "50%": False, "75%": False}, 
        "graphs": 
                {"scatter": False, "hist": False, "corr": False, "heatmap": False, "dotplot": False, "linear": False,"box": False,  
                "piechart": False, "log": False, "multihist": False},
        "data": 
                {"preprocessing": 
                    {"fillna": "mean", "encoding": "label_encoding", "scaling": False},
                "path": "C:\\Users\\egorl\\Desktop\\Глаукому", "fillna": "mean"}}, 
        "MODULE": "STATS"}



    data_json['graphs'] = data_json.pop('graphics')
    data_json['data'] = {
        'preprocessing': {
            "fillna": ["mean", "exact_value", 'dropna','median'][data_json['dataPrepOption']],
            "encoding": "label_encoding", 
            "scaling": bool(data_json.pop('dataPrepOption'))}, 
        'path': data_json.pop('data')
        }

    data_json['data']['fillna'] = data_json['data']['preprocessing']['fillna']
    data_json['MODULE_SETTINGS'] = {
        'metrics': data_json.pop('metrics'),
        'graphs': data_json.pop('graphs'), 
        'data': data_json.pop('data')
        }
    data_json['MODULE'] = 'STATS'
    for settings in ['metrics', 'graphs']:
        tmp_lst = sorted(data_json["MODULE_SETTINGS"][settings])
        data_json["MODULE_SETTINGS"][settings] = json_example["MODULE_SETTINGS"][settings]
        for sett in tmp_lst:
            if sett == 5 and settings == 'metrics':
                data_json["MODULE_SETTINGS"][settings]["25%"] = True
                data_json["MODULE_SETTINGS"][settings]["50%"] = True
                data_json["MODULE_SETTINGS"][settings]["75%"] = True
                continue
            data_json["MODULE_SETTINGS"][settings][list(json_example["MODULE_SETTINGS"][settings].keys())[sett]] = True


    #data_json['MODULE_SETTINGS']['data']['path'] = 'C:\\Users\\egorl\\Desktop\\Глаукому.xlsx'
    module_starter = ModuleManipulator(data_json)
    threading.Thread(target=module_starter.start, daemon=True).start()
    return 'get'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=13000, debug=True)
