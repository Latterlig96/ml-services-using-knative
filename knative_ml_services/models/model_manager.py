import pandas as pd
from sklearn.svm import SVR
import xgboost
from typing import Tuple, Any, Optional, Union, Dict
from knative_ml_services.client.mlflow_client import MlClient
from knative_ml_services.utils import preprocess_data
from joblib import dump, load


class ModelManager:

    @MlClient.build_from_env()
    def __init__(self, client: MlClient, model_type: str, config: Dict[str, Any]):
        self._client = client
        self._model_type = model_type
        self._config = config
        self._client.configure_autolog(self._model_type)

    def prepare_data(self, data: pd.DataFrame, target: pd.Series) -> Tuple:
        if self._model_type.lower() == "xgb":
            return xgboost.DMatrix(data, label=target, enable_categorical=True),
        else:
            return data, target

    def train_model(self, data: Any, target: Optional[pd.Series] = None):
        if self._model_type.lower() == "xgb":
            trained_model = xgboost.train(**self._config, dtrain=data)
        else:
            trained_model = SVR(**self._config).fit(data, target)
        return trained_model

    def save_model(self, model: Any, save_path: str) -> None:
        dump(model, save_path)

    @staticmethod
    def load_model(load_object: Union[str, bytes]):
        return load(load_object)

    @staticmethod
    def create_predictions(model_name: str, model: Any, data: Any):
        if isinstance(data, dict):
            data = preprocess_data(pd.json_normalize(data), model_name)
        if model_name.lower() == "xgb":
            prepared_data = xgboost.DMatrix(data, enable_categorical=True)
            return model.predict(prepared_data)
        else:
            prepared_data = data.to_numpy()
            return model.predict(prepared_data)
