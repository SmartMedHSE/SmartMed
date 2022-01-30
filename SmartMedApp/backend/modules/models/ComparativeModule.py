from .ModuleInterface import Module
from .dash import ComparativeDashboard

from .dataprep import PandasPreprocessor


class StatisticsModule(Module, ComparativeDashboard):

    def _prepare_data(self):
        # custom class preprocessor with pandas
        self.pp = PandasPreprocessor(self.settings['data'])
        self.pp.fillna()
        return self.pp.df

    def _prepare_dashboard_settings(self):
        # settings = dict()

        settings = {'data_type': 'continuous', 'comparison_method': ['T-criterion of Student',
                                                                     'U-criterion of Mann-Whitney',
                                                                     'T-criterion of Wilcoxon']}
        # create dashboard dict settings
        self.settings['criterion'] = ['T-criterion of Student', 'U-criterion of Mann-Whitney',
                                      'T-criterion of Wilcoxon']

        self.graph_to_method = {
            'T-criterion of Student': self._generate_t_criterion_student,
            'U-criterion of Mann-Whitney': self._generate_u_criterion_mann_whitney,
            'T-criterion of Wilcoxon': self._generate_t_criterion_wilcoxon,
        }

        settings['data'] = self.data

        return settings

    def _prepare_dashboard(self):
        pass
