import os
import sys

from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, request

from GUI.apps.utils import read_file
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

BIOEQ_NORMALITY = {
    0: 'Kolmogorov',
    1: 'Shapiro'
}

BIOEQ_DESIGN = {
    0: 'cross',
    1: 'parallel'
}

BIOEQ_UNIFORMITY = {
    0: 'F',
    1: 'Leven'
}

cache: dict = {}


def change_cache(key, val):
    cache[key] = val


def get_cache_val(key):
    return cache[key]


def run_dash(dash_count):
    data = get_cache_val("data")
    module = ModuleManipulator(data).start()
    app = module.app
    application.mounts[f"/app{dash_count}"] = app.server


@server.route('/api/descriptive', methods=['POST'])
def get_descriptive_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        metrics_dict = data_json['metrics']
        graphs_dict = data_json['graphics']
        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]


        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        prepared_data = {
            "MODULE": "STATS",
            "MODULE_SETTINGS":
                {
                    "server": server,
                    "url_count": get_cache_val('cnt'),
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

        change_cache(key='data', val=prepared_data)

        run_dash(get_cache_val("cnt"))

        return "good"


@server.route('/api/comparative', methods=['POST'])
def get_comparative_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]
        vat_type = 'categorical' if data_json['var_type'] else 'continuous'
        continuous_methods = data_json['continuous_methods']
        categorial_methods = data_json['categorial_methods']

        if vat_type == 'categorical':
            comparative_methods = {
                'pearson': categorial_methods['0'],
                'se_sp': categorial_methods['1'],
                'odds_ratio': categorial_methods['2'],
                'risk_ratio': categorial_methods['3']
            }
        else:
            comparative_methods = {
                'kolmagorova_smirnova': continuous_methods['0'],
                'student_independent': continuous_methods['1'],
                'student_dependent': continuous_methods['2'],
                'mann_whitney': continuous_methods['3'],
                'wilcoxon': continuous_methods['4']
            }


        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        prepared_data = {
            "MODULE": "COMPARATIVE",
            "MODULE_SETTINGS":
                {
                    'path': data_json['filePath'],
                    'columns': read_file(data_json['filePath']).columns,
                    'preprocessing': data_prep_option,
                    'type': vat_type,
                    'methods': comparative_methods,

                    "server": server,
                    "url_count": get_cache_val('cnt'),
                }
        }
        print(f"{prepared_data=}")

        change_cache(key='data', val=prepared_data)

        run_dash(get_cache_val("cnt"))

        return "good"


@server.route('/api/bioequivalence', methods=['POST'])
def get_bioequivalence_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        plan = data_json['plan']
        method = data_json['method']
        homogeneity_method = data_json['homogeneity_method']

        first_file = data_json['fileOne']
        second_file = data_json['fileTwo']
        normality = BIOEQ_NORMALITY[method]
        design = BIOEQ_DESIGN[plan]
        cross_table = data_json['table']
        cross_graphs = data_json['visualisation']
        uniformity = BIOEQ_UNIFORMITY[homogeneity_method]
        paral_graphs = data_json['paral_graphics']
        paral_table = data_json['paral_table']


        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)
        if plan:
            prepared_data = {
                "MODULE": "BIOEQ",
                "MODULE_SETTINGS":
                {
                    'path_test': first_file,
                    'path_ref': second_file,
                    'design': design,
                    'normality': normality,
                    'uniformity': uniformity,
                    'tables':
                     {
                         'criteria': paral_table['0'],
                         'features': paral_table['1'],
                         'var': paral_table['2'],
                         'statistics': paral_table['4']
                     },
                    'graphs':
                    {
                        'all_in_group': paral_graphs['0'],
                        'log_all_in_group': paral_graphs['1'],
                        'each_in_group': paral_graphs['2'],
                        'log_each_in_group': paral_graphs['3']
                    },

                    "server": server,
                    "url_count": get_cache_val('cnt'),
                }
            }
        else:
            prepared_data = {
                "MODULE": "BIOEQ",
                "MODULE_SETTINGS":
                {
                    'path_test': first_file,
                    'path_ref': second_file,
                    'design': design,
                    'normality': normality,
                    'tables':
                    {
                        'avg_auc': cross_table['0'],
                        'anal_resylts': cross_table['1'],
                        'results': cross_table['2'],
                        'statistics': cross_table['3']
                    },
                    'graphs':
                    {
                        'indiv_concet': cross_graphs['0'],
                        'avg_concet': cross_graphs['1'],
                        'gen_concet': cross_graphs['2']
                    },

                    "server": server,
                    "url_count": get_cache_val('cnt'),
                }
            }
        print(f"{prepared_data=}")

        change_cache(key='data', val=prepared_data)

        run_dash(get_cache_val("cnt"))

        return "good"


if __name__ == '__main__':
    run_simple("localhost", 15001, application, use_debugger=True, use_reloader=True, threaded=True)
