import os
import sys

import dash
import dash_html_components as html
from werkzeug import run_simple
import dash_table
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from dash import Dash
from flask import Flask, request

from backend.ModuleManipulator import ModuleManipulator

BASE_DIR = os.path.abspath(os.curdir)
sys.path.append(BASE_DIR)

server = Flask(__name__)
# server.suppress_callback_exceptions = True

application = DispatcherMiddleware(server, {})

DATA_PREP_OPTIONS = {
    0: 'mean',
    1: 'exact_value',
    2: 'dropna',
    3: 'median'
}

cache: dict = {}


def change_cache(key, val):
    cache[key] = val


def get_cache_val(key):
    return cache[key]


@server.route('/api/comparative', methods=['POST'])
def get_comparative_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}\n\n")

        file_path = data_json['filePath']
        categorial_methods_dict = data_json['categorial_methods']
        continuous_methods_dict = data_json['continuous_methods']
        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]

        # prepared_data = {
        #     "MODULE": "STATS",
        #     "MODULE_SETTINGS":
        #         {
        #             "metrics":
        #                 {
        #                     "count": metrics_dict['0'],
        #                     "mean": metrics_dict['1'],
        #                     "std": metrics_dict['2'],
        #                     "max": metrics_dict['3'],
        #                     "min": metrics_dict['4'],
        #                     "25%": metrics_dict['5'],
        #                     "50%": metrics_dict['5'],
        #                     "75%": metrics_dict['5']
        #                 },
        #             "graphs":
        #                 {
        #                     "scatter": graphs_dict['0'],
        #                     "hist": graphs_dict['1'],
        #                     "corr": graphs_dict['2'],
        #                     "heatmap": graphs_dict['3'],
        #                     "dotplot": graphs_dict['4'],
        #                     "linear": graphs_dict['5'],
        #                     "box": graphs_dict['6'],
        #                     "piechart": graphs_dict['8'],
        #                     "log": graphs_dict['9'],
        #                     "multihist": graphs_dict['10']
        #                 },
        #             "data":
        #                 {
        #                     "preprocessing":
        #                         {
        #                             "fillna": data_prep_option,
        #                             "encoding": "label_encoding",
        #                             "scaling": False
        #                         },
        #                     "path": file_path,
        #                     "fillna": data_prep_option
        #                 }
        #         }
        # }

        # print(f"{prepared_data=}")
        #
        #
        # change_cache(key='data', val=prepared_data)

        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        return run_dash(get_cache_val("cnt"))


# @server.route('/dash/<dash_count>')
def run_dash(dash_count):
    data = get_cache_val("data")
    module = ModuleManipulator(data).start()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    external_scripts = [
        'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']

    app = Dash(__name__, server=server, url_base_pathname=f"/dash{dash_count}/",
               external_stylesheets=external_stylesheets, external_scripts=external_scripts)

    app.layout = module.app.layout

    print(f"/dash{dash_count}/")
    # print(f"{dir(app)=}")
    print(f"{dir(module.app)=}")
    #
    # print(app.callback_map)
    # print(app.scripts)
    # print(app.routes)
    # print(app.config)
    # print(app.serve_layout())
    # print(app.serve_reload_hash())
    # print(app.registered_paths)

    # module.app.registered_paths = app.registered_paths
    # app = module.app
    print()
    # print(app.callback_map)
    # print(app.scripts)
    # print(app.routes)
    # print(app.config)
    # print(app.serve_layout())
    # print(app.serve_reload_hash())
    # print(app.registered_paths)

    application.mounts[f"/app{dash_count}"] = app.server
    print(application.mounts)

    # app.suppress_callback_exceptions = True

    # return app.index()


@server.route('/api/descriptive', methods=['POST'])
def get_descriptive_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        metrics_dict = data_json['metrics']
        graphs_dict = data_json['graphics']
        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]

        prepared_data = {
            "MODULE": "STATS",
            "MODULE_SETTINGS":
                {
                    "metrics":
                        {
                            "count": metrics_dict['0'],
                            "mean": metrics_dict['1'],
                            "std": metrics_dict['2'],
                            "max": metrics_dict['3'],
                            "min": metrics_dict['4'],
                            "25%": metrics_dict['5'],
                            "50%": metrics_dict['5'],
                            "75%": metrics_dict['5']
                        },
                    "graphs":
                        {
                            "scatter": graphs_dict['0'],
                            "hist": graphs_dict['1'],
                            "corr": graphs_dict['2'],
                            "heatmap": graphs_dict['3'],
                            "dotplot": graphs_dict['4'],
                            "linear": graphs_dict['5'],
                            "box": graphs_dict['6'],
                            "piechart": graphs_dict['8'],
                            "log": graphs_dict['9'],
                            "multihist": graphs_dict['10']
                        },
                    "data":
                        {
                            "preprocessing":
                                {
                                    "fillna": data_prep_option,
                                    "encoding": "label_encoding",
                                    "scaling": False
                                },
                            "path": data_json['filePath'],
                            "fillna": data_prep_option
                        }
                }
        }
        print(f"{prepared_data=}")

        # module_starter = ModuleManipulator(prepared_data)
        # proc = multiprocessing.Process(target=module_starter.start).start()

        change_cache(key='data', val=prepared_data)

        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        run_dash(get_cache_val("cnt"))
        # return run_dash(get_cache_val("cnt"))
        return "good"


if __name__ == '__main__':
    run_simple("localhost", 15001, application, use_debugger=True, use_reloader=True, threaded=True)
    # server.run(port=15001, debug=False)
