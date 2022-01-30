from .Dashboard import Dashboard

import dash_html_components as html
import dash_core_components as dcc
import dash
import dash_table
import numpy as np
import pandas as pd

class ComparativeDashboard(Dashboard):

    def _generate_layout(self):
        # metrics inludings is checked inside method
        graph_list = []
        for graph in self.settings['criterion']:
            graph_list.append(self.graph_to_method[graph]())

        return html.Div(graph_list)

    def _generate_t_criterion_student(self):

        def get_average(data):
            return data.sum() / len(data)

        def get_sample_variance(data):
            return (data - get_average(data)) ** 2 / (len(data) - 1)

        def get_empirical_value_t(x, y):
            m_x = get_average(x)
            m_y = get_average(y)
            s_x_2 = get_sample_variance(x)
            s_y_2 = get_sample_variance(y)
            n_x = len(x)
            n_y = len(y)

            return abs(m_x - m_y) / (np.sqrt(s_x_2 / n_x + s_y_2 / n_y))

        def get_freedom_degree(x, y):
            s_x_2 = get_sample_variance(x)
            s_y_2 = get_sample_variance(y)
            n_x = len(x)
            n_y = len(y)

            if s_x_2 / s_y_2 > 10 or s_y_2 / s_x_2 > 10:
                f = (n_x + n_y - 2) * (0.5 + s_x_2 * s_y_2 / (s_x_2 ** 2 + s_y_2 ** 2))
            else:
                f = n_x + n_y - 2

            return f

        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        results = [get_empirical_value_t(x, y), get_freedom_degree(x, y)]
        df = pd.DataFrame(data=results, columns=['t', 'Степень свободы'])

        return html.Div(html.H4(children='Т-критерий Стьюдента'),
                     style={'text-align': 'center'}), \
               html.Div([
                   html.Div(dash_table.DataTable(
                       id='table_t_criterion_student',
                       columns=[{"name": i, "id": i} for i in df.columns],
                       data=df.to_dict('records'),
                       export_format='csv'),
                       style={'border-color': 'rgb(220, 220, 220)', 'border-style': 'solid', 'text-align': 'center',
                              'width': str(len(df.columns) * 10 - 10) + '%', 'display': 'inline-block'}),
                   html.Div(dcc.Markdown(roc_table_metrics))])

    def _generate_u_criterion_mann_whitney(self):
        pass

    def _generate_t_criterion_wilcoxon(self):
        pass

