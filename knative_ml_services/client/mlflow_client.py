import mlflow
from mlflow import MlflowClient
import os


class MlClient:

    def __init__(self,
                 tracking_uri: str,
                 registry_uri: str):
        self._client = MlflowClient(tracking_uri, registry_uri)

    @property
    def client(self):
        return self._client

    def configure_autolog(self, model_type: str):
        if model_type == "XGB":
            mlflow.xgboost.autolog()
        else:
            mlflow.sklearn.autolog()

    @classmethod
    def build_from_env(cls):
        tracking_uri = os.getenv("MLFLOW_TRACKING_URI", None)
        registry_uri = os.getenv("REGISTRY_URI", None)
        return MlClient(tracking_uri, registry_uri)

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            return fn(*args, client=self, **kwargs)
        return wrapper
