from typing import Optional

import numpy as np
import pandas as pd
import joblib
from mlflow.pyfunc import PythonModel, PythonModelContext


# Reference: https://mlflow.org/docs/latest/python_api/mlflow.pyfunc.html
class SentimentClassifier(PythonModel):
    def __init__(self):
        self.vectorizer = None
        self.model = None
    
    # Optional
    # When loading an MLflow model with load_model(), this method is called as soon as the PythonModel is constructed.
    def load_context(self, context: PythonModelContext):
        self.model = joblib.load(context.artifacts["model"])
        self.vectorizer = joblib.load(context.artifacts["vectorizer"])
    
    # mandatory
    def predict(
        self,
        context: Optional[PythonModelContext],
        input_df: pd.DataFrame
    ) -> np.ndarray:
        return self.custom_predict(input_df)
    
    def custom_predict(self, input_df: pd.DataFrame) -> np.ndarray:
        inputs = self.vectorizer.transform(input_df["review"])
        return self.model.predict(inputs)