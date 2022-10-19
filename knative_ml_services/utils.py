import json
import pandas as pd
from typing import List, Union


def get_object_columns(data: pd.DataFrame) -> List[int]:
    object_columns = []
    for i in data.columns:
        if data[i].dtype == object:
            object_columns.append(i)
    return object_columns


def load_model_config(data: Union[str, bytes]):
    if isinstance(data, bytes):
        return json.loads(data)
    with open(data, "rb") as f:
        return json.loads(f.read())


def preprocess_data(data: pd.DataFrame, model_type: str) -> pd.DataFrame:
    object_columns = get_object_columns(data)
    num_columns = list(set(list(data.columns)) - set(object_columns))
    object_data = data[object_columns]
    num_data = data[num_columns]
    for i in object_columns:
        object_data[i].fillna("No", inplace=True)
        object_data[i] = object_data[i].rank()
        data[i] = object_data[i]
    for i in num_columns:
        num_data[i].fillna(0, inplace=True)
        data[i] = num_data[i]
    return data
