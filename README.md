# Knative ml service

Simple project that aims to train skills regarding kubernetes and microservices architecture with the use of [Knative](https://knative.dev/docs/)

## Prerequisites
* Installed docker with version 20.10.18
* Minikube installed with version 1.28.0
* Knative installed and deployed ([Installation Guide](https://knative.dev/docs/install/)) (use Kourier as a load balancer)
* Ubuntu 22.04 (for Windows users there might be some tweaking regarding having WSL installed to use docker runtime for minikube)

## Dataset
To train models (which are XGBoost and SVM) I used kaggle dataset that can be found under the [link](https://www.kaggle.com/datasets/yasserh/housing-prices-dataset)


## How to run
To create whole deployment I use Makefile so only thing that is needed to run is to type `make` in main project dir. \
NOTE: To run deployment you have to first have trained models on dataset managed in dataset section and have them stored on s3 bucket configured in `configmap` (see [configmap](minikube/configmap/project_config.yaml))

## Tech stack
* Kubernetes <img src=".github/.idea/kubernetes.svg.png" width=100></img>
* Knative <img src=".github/.idea/knative.png" width=100></img>
* Minikube <img src=".github/.idea/minikube.png" width=100></img>
* Docker <img src=".github/.idea/docker.svg.png" width=200></img>
* FastAPI <img src=".github/.idea/fastapi.svg" width=100></img>
* Minio <img src=".github/.idea/minio.svg" width=50></img>

## Further improvements
Given the fact that this project aimed to be a PoC sample project I don't have any plan for further improvements.