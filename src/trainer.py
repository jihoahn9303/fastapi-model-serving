from typing import List, Tuple

import numpy as np
from matplotlib.figure import Figure
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from utils.figure import draw_confusion_matrix


def train(
    train_inputs: csr_matrix,
    train_labels: np.ndarray,
    **model_kwargs
) -> BaseEstimator:
    model = LogisticRegression(**model_kwargs)
    model.fit(train_inputs, train_labels)
    
    return model

def evaluate(
    model: BaseEstimator,
    test_inputs: csr_matrix,
    test_labels: np.ndarray,
    class_names: List[str]
) -> Tuple[float, Figure]:
    predictions = model.predict(test_inputs)
    figure = draw_confusion_matrix(
        test_labels,
        predictions,
        class_names
    )
    
    return f1_score(test_labels, predictions), figure