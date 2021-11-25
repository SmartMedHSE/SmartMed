import numpy as np
from sklearn.tree import DecisionTreeClassifier

from .BaseModel import BaseModel


class TreeModel(BaseModel):

    def __init__(self, x, y, extra_param):
        if extra_param is None:
            extra_param = np.array([None, 2, None])
        super().__init__(DecisionTreeClassifier, x, y, extra_param)
