from typing import Dict

from .modules import *


class ModuleChoiceException(Exception):
    pass


class ModuleManipulator:

    def __init__(self, settings: Dict):
        self.settings = settings

    def start(self):
        print('START settings')
        print(self.settings)
        print('END settings')

        if self.settings['MODULE'] == 'STATS':
            module = StatisticsModule(self.settings['MODULE_SETTINGS'])
        elif self.settings['MODULE'] == 'PREDICT':
            module = PredictionModule(self.settings['MODULE_SETTINGS'])
        elif self.settings['MODULE'] == 'BIOEQ':
            module = BioequivalenceModule(self.settings['MODULE_SETTINGS'])
        elif self.settings['MODULE'] == 'COMPARATIVE':
            module = ComparativeModule(self.settings['MODULE_SETTINGS'])
        else:
            raise ModuleChoiceException

        module.run()
        return module
