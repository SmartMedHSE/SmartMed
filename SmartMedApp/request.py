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
    json_request = None
    if request.method == 'POST':
        json_request = request.json

    base_response = {
        "MODULE_SETTINGS": 
        {"metrics": 
            {"count": False, "mean": False, "std": False, "max": False, "min": False, "25%": False, 
            "50%": False, "75%": False}, 
        "graphs": 
                {"scatter": False, "hist": False, "corr": False, "heatmap": False, "dotplot": False, "linear": False,"box": False,  
                "piechart": False, "log": False, "multihist": False},
        "data": 
                {"preprocessing": 
                    {"fillna": None, "encoding": "label_encoding", "scaling": False},
                "path": None, "fillna": None}}, 
        "MODULE": "STATS"}


    json_request["graphs"] = json_request.pop("graphics") #Замена на одноименный ключ в шаблонном словаре
    base_settings = base_response["MODULE_SETTINGS"] #Замена переменной для читаемости кода


    for key_from_response in json_request:
        if key_from_response == 'data': #Присваиваем значение путя к файлу
            base_settings['data']['path'] = json_request['data']


        elif key_from_response == 'dataPrepOption':#Присваиваем значение предобработки из файла
            list_of_prep = ["mean", "exact_value", 'dropna','median'] #Список способов предобработки
            choose_of_prep = json_request['dataPrepOption'] #Индекс из списка способов предобработки
            base_settings['data']['preprocessing']['fillna'] = list_of_prep[choose_of_prep]
            base_settings['data']['fillna'] = list_of_prep[choose_of_prep]


        elif key_from_response in ['metrics','graphs']: #Перебираем выбранные метрики пользователем
            #Массив из значений ключей метрик или графиков шаблонного запроса
            key_of_metrics = list(base_settings[key_from_response].keys())
            for user_metrics in sorted(json_request[key_from_response]): #Перебираем значения метрик или графиков пользователя и выбираем их в шаблонном запросе
                #Т.е. выбираем ключ из ключей метрик или графиков, соотвествующий номеру из запроса и присваиваем ему True
                tmp_name_of_metric = key_of_metrics[user_metrics]
                base_settings[key_from_response][tmp_name_of_metric] = True
        
    if base_settings['metrics']['25%']: #Если выбран квантиль 25%, то за ним выбираются 50 и 75
        base_settings['metrics']['50%'] = True
        base_settings['metrics']['75%'] = True

    print(base_response)
    module_starter = ModuleManipulator(base_response)
    threading.Thread(target=module_starter.start, daemon=True).start()
    return 'get'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=13000, debug=True)
