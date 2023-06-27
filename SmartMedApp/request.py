import json
import os
import sys

from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, request

from GUI.apps.utils import read_file, get_class_columns
from backend.ModuleManipulator import ModuleManipulator

BASE_DIR = os.path.abspath(os.curdir)
sys.path.append(BASE_DIR)

server = Flask(__name__)
# server.suppress_callback_exceptions = True

application = DispatcherMiddleware(server, {})

DATA_PREP_OPTIONS = {
    0: 'mean',
    1: 'dropna',
    2: 'median'
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


@server.route('/api/predictive/get_class_columns', methods=['POST'])
def class_columns_api():
    if request.method == 'POST':
        data_json = request.json
        print(data_json)
        file_path = data_json['filePath']

        index_columns = get_class_columns(file_path, 11)

        return (json.dumps(list(index_columns)), 200)


@server.route('/api/predictive', methods=['POST'])
def get_predictive_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        dependent_val = data_json['dependent_val']
        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]
        file_path = data_json['filePath']
        table_and_graph_options = data_json['table_and_graph_options']
        regression_model = data_json['regression_model']
        log_reg_table_and_graph_options = data_json['table_and_graph_options']
        roc_metrics = data_json['roc_metrics']
        roc_graphics_and_tables = data_json['roc_graphics_and_tables']
        poly_reg_table_and_graph_options = data_json['table_and_graph_options']
        tree_graphics_and_tables = data_json['tree_graphics_and_tables']

        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        if regression_model == 0:
            prepared_data = {
                "MODULE": "PREDICT",
                "MODULE_SETTINGS":
                {
                    "server": server,
                    "url_count": get_cache_val('cnt'),

                    'path': file_path,
                    'preprocessing': data_prep_option,
                    'model': 'linreg',
                    'variable': dependent_val,

                    'distrib_resid': table_and_graph_options['4'],
                    'equation': table_and_graph_options['2'],
                    'model_quality': table_and_graph_options['0'],
                    'resid': table_and_graph_options['3'],
                    'signif': table_and_graph_options['1'],
                }
            }
        elif regression_model == 1:
            prepared_data = {
                "MODULE": "PREDICT",
                "MODULE_SETTINGS":
                    {
                        "server": server,
                        "url_count": get_cache_val('cnt'),

                        'path': file_path,
                        'preprocessing': data_prep_option,
                        'model': 'logreg',
                        'variable': dependent_val,

                        'distrib_resid': log_reg_table_and_graph_options['4'],
                        'equation': log_reg_table_and_graph_options['2'],
                        'model_quality': log_reg_table_and_graph_options['0'],
                        'resid': log_reg_table_and_graph_options['3'],
                        'signif': log_reg_table_and_graph_options['1'],
                    }
            }
        elif regression_model == 2:
            prepared_data = {
                "MODULE": "PREDICT",
                "MODULE_SETTINGS":
                    {
                        "server": server,
                        "url_count": get_cache_val('cnt'),

                        'path': file_path,
                        'preprocessing': data_prep_option,
                        'model': 'tree',
                        'variable': dependent_val,

                        'tree_depth': 5,
                        'samples': 5,
                        'features_count': 2,
                        'sort': True,
                        'tree': tree_graphics_and_tables['0'],
                        'table': tree_graphics_and_tables['1'],
                        'indicators': tree_graphics_and_tables['2'],
                        'distributions': tree_graphics_and_tables['3'],
                        'prediction': tree_graphics_and_tables['4']
                    }
            }
        elif regression_model == 3:
            prepared_data = {
                "MODULE": "PREDICT",
                "MODULE_SETTINGS":
                    {
                        "server": server,
                        "url_count": get_cache_val('cnt'),

                        'path': file_path,
                        'preprocessing': data_prep_option,
                        'model': 'roc',
                        'variable': dependent_val,

                        'accuracy': roc_metrics['3'],
                        'confidence': roc_metrics['5'],
                        'F': roc_metrics['4'],
                        'precision': roc_metrics['2'],
                        'sensitivity': roc_metrics['1'],
                        'trashhold': roc_metrics['0'],
                        'specificity': roc_metrics['6'],

                        'points_table': roc_graphics_and_tables['0'],
                        'metrics_table': roc_graphics_and_tables['1'],
                        'spec_and_sens': roc_graphics_and_tables['2'],
                        'spec_and_sens_table': roc_graphics_and_tables['3'],
                        'classificators_comparison': roc_graphics_and_tables['4']
                    }
            }
        elif regression_model == 4:
            prepared_data = {
                "MODULE": "PREDICT",
                "MODULE_SETTINGS":
                    {
                        "server": server,
                        "url_count": get_cache_val('cnt'),

                        'path': file_path,
                        'preprocessing': data_prep_option,
                        'model': 'polynomreg',
                        'variable': dependent_val,

                        'distrib_resid': poly_reg_table_and_graph_options['4'],
                        'equation': poly_reg_table_and_graph_options['2'],
                        'model_quality': poly_reg_table_and_graph_options['0'],
                        'resid': poly_reg_table_and_graph_options['3'],
                        'signif': poly_reg_table_and_graph_options['1'],
                    }
            }
        print(f"{prepared_data=}")

        change_cache(key='data', val=prepared_data)

        run_dash(get_cache_val("cnt"))

        return "good"

@server.route('/api/cluster', methods=['POST'])
def get_cluster_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        metrics_dict = data_json['metric']
        graphs_dict = data_json['methodType']
        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]


        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        prepared_data = {
            "MODULE": "CLUSTER",
            "MODULE_SETTINGS":
                {
                    "server": server,
                    "url_count": get_cache_val('cnt'),
 
                     "path": data_json['filePath'],
                     "fillna": data_prep_option,
                     "metric": metrics_dict,
                     "method": graphs_dict,
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


@server.route('/api/lifeline', methods=['POST'])
def get_lifeline_params():
    if request.method == 'POST':
        data_json = request.json
        print(f"{data_json=}")

        methods_dict = data_json['methods']
        criteria_dict = data_json['criteria']
        model = data_json['regression_model']
        data_prep_option = DATA_PREP_OPTIONS[data_json['dataPrepOption']]

        try:
            change_cache(key='cnt', val=get_cache_val("cnt") + 1)
        except:
            change_cache(key='cnt', val=0)

        prepared_data = {
            "MODULE": "LIFELINE",
            "MODULE_SETTINGS":
                {
                    "server": server,
                    "url_count": get_cache_val('cnt'),

                    "path": data_json['filePath'],
                    "fillna": data_prep_option,
                    "model": model,
                    "criteria": criteria_dict,
                    "method": methods_dict,
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


if __name__ == '__main__':
    run_simple("localhost", 15001, application, use_debugger=True, use_reloader=True, threaded=True)
