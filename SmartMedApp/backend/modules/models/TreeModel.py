from sklearn.tree import DecisionTreeClassifier

from .BaseModel import BaseModel


class TreeModel(BaseModel):

    def __init__(self, x, y):
        super().__init__(DecisionTreeClassifier, x, y)