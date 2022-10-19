import os
import io
import re
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from knative_ml_services.__version__ import __version__
from knative_ml_services.client.minio_client import MinioClient
from knative_ml_services.models.model_manager import ModelManager

app = FastAPI()

model_container = {}


@app.on_event("startup")
def load_models():
    minio_client = MinioClient.build_from_env()
    models_path = os.getenv("MODEL_PATHS").split(" ")
    for model_path in models_path:
        if "s3" in model_path:
            bucket_name = model_path.split("//")[1].split("/")[0]
            object_path = model_path.split("//")[1].replace(bucket_name, "")
            model_content = io.BytesIO(minio_client.get_object_from_bucket(bucket_name, object_path))
            model = ModelManager.load_model(model_content)
        else:
            model = ModelManager.load_model(model_path)
        model_container[re.sub("\..*", "", model_path).split("/")[-1]] = model
    return model_container


@app.get("/")
async def index():
    return {"api_version": __version__, "dev": True}


@app.post("/models/{model_name}/predict")
async def predict(model_name: str, request: Request):
    content = await request.json()
    model_name = model_name.lower()
    model = model_container[model_name]
    prediction = ModelManager.create_predictions(model_name, model, content)[0]
    return {"prediction": float(prediction)}


def main():
    uvicorn.run(os.getenv("APP_HANDLER"), host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")), log_level="info")
