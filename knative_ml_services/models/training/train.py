import pandas as pd
import argparse
from knative_ml_services.client.minio_client import MinioClient
from knative_ml_services.models.model_manager import ModelManager
from knative_ml_services.utils import preprocess_data, load_model_config
import subprocess


parser = argparse.ArgumentParser("Sample Training script")

parser.add_argument("--train-data",
                    dest="train_data",
                    type=str,
                    help="Path for input data")

parser.add_argument("--valid-data",
                    dest="valid_data",
                    type=str,
                    default=None,
                    help="Path for validation data")

parser.add_argument("-m",
                    "--model",
                    dest="model",
                    type=str,
                    help="Model type to use during training")

parser.add_argument("-c",
                    "--config",
                    dest="config",
                    type=str,
                    help="Config path to use for given model")

parser.add_argument("-s",
                    "--save-path",
                    dest="save_path",
                    type=str,
                    help="Name of the bucket to save model")


def main():
    args = parser.parse_known_args()[0]

    input_data = pd.read_csv(args.__dict__["train_data"])
    input_train_data = preprocess_data(input_data, args.__dict__["model"])
    minio_client = MinioClient.build_from_env()

    config_path = args.__dict__["config"]
    if "s3" in config_path:
        bucket_name = config_path.split("//")[1].split("/")[0]
        minio_client.create_bucket(bucket_name)
        object_name = config_path.split("//")[1].replace(bucket_name, "")
        config_content = minio_client.get_object_from_bucket(bucket_name, object_name)
        model_config = load_model_config(config_content)
    else:
        model_config = load_model_config(config_path)

    x = input_train_data.drop(["Id", "SalePrice"], axis=1)
    x.iloc[0].to_json("sample.json")
    y = input_train_data["SalePrice"]

    model_manager = ModelManager(model_type=args.__dict__["model"], config=model_config)
    prepared_data = model_manager.prepare_data(x, y)
    if args.model.lower() == "xgb":
        trained_model = model_manager.train_model(data=prepared_data[0])
    else:
        trained_model = model_manager.train_model(data=prepared_data[0], target=prepared_data[1])

    save_path = args.__dict__["save_path"]
    if "s3" in args.save_path:
        bucket_name = save_path.split("//")[1].split("/")[0]
        minio_client.create_bucket(bucket_name)
        s3_save_path = save_path.split("//")[1].replace(bucket_name, "")
        local_save_path = save_path.split("/")[-1]
        model_manager.save_model(trained_model, local_save_path)
        minio_client.put_object_to_bucket(bucket_name, s3_save_path, local_save_path)
        subprocess.run(["rm", local_save_path])
    else:
        model_manager.save_model(trained_model, save_path)
