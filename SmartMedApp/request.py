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

    json_example = {
        "MODULE_SETTINGS":
            {"metrics":
                 {"count": None, "mean": None, "std": None, "max": None, "min": None, "25%": None,
                  "50%": None, "75%": None},
             "graphs":
                 {"scatter": None, "hist": None, "corr": None, "heatmap": None, "dotplot": None, "linear": None,
                  "box": None,
                  "piechart": None, "log": None, "multihist": None},
             "data":
                 {"preprocessing":
                      {"fillna": None, "encoding": "label_encoding", "scaling": False},
                  "path": None, "fillna": None}},
        "MODULE": None}

    data_json['graphs'] = data_json.pop('graphics')
    data_json['data'] = {
        'preprocessing': {
            "fillna": ["mean", "exact_value", 'dropna', 'median'][data_json['dataPrepOption']],
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
    # Перебираем ключи, значения для которых нужно изменить
    for settings in ['metrics', 'graphs']:
        # Сохряняем пользв. выбор в отдельную переменную, отсортировав по порядку
        tmp_lst = sorted(data_json["MODULE_SETTINGS"][settings])
        data_json["MODULE_SETTINGS"][settings] = json_example["MODULE_SETTINGS"][settings]
        # Словарь ключей settings
        list_of_keys = list(json_example["MODULE_SETTINGS"][settings].keys())
        for sett in tmp_lst:
            if sett == 5 and settings == 'metrics':
                data_json["MODULE_SETTINGS"][settings]["25%"] = True
                data_json["MODULE_SETTINGS"][settings]["50%"] = True
                data_json["MODULE_SETTINGS"][settings]["75%"] = True
                continue
            # Отмечаем выбранные пользователем параметры
            data_json["MODULE_SETTINGS"][settings][list_of_keys[sett]] = True

    module_starter = ModuleManipulator(data_json)
    threading.Thread(target=module_starter.start, daemon=True).start()
    return 'get'


if __name__ == '__main__':
    app.run(port=13000, debug=True)
