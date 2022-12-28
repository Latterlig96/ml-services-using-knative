DOCKER = docker
KUBERNETES_OPERATOR = minikube
KUBERNETES_CLIENT = kubectl

all: build_dockerfile pull_mlflow load_to_minikube build_config build_minio build_postgres build_mlflow build_knative

build_dockerfile:
	${DOCKER} build --tag knative-ml-service:latest .

pull_mlflow:
	${DOCKER} pull pdemeulenaer/mlflow-server:537

load_to_minikube:
	${KUBERNETES_OPERATOR} image load knative-ml-service:latest
	${KUBERNETES_OPERATOR} image load pdemeulenaer/mlflow-server:537

build_config:
	${KUBERNETES_CLIENT} apply -f minikube/configmap/project_config.yaml

build_minio:
	${KUBERNETES_CLIENT} apply -f minikube/volumes/minio_volume.yaml
	${KUBERNETES_CLIENT} apply -f minikube/deployments/minio_deployment.yaml
	${KUBERNETES_CLIENT} apply -f minikube/services/minio_service.yaml

build_postgres:
	${KUBERNETES_CLIENT} apply -f minikube/volumes/postgres_volume.yaml
	${KUBERNETES_CLIENT} apply -f minikube/deployments/postgres_deployment.yaml
	${KUBERNETES_CLIENT} apply -f minikube/services/postgres_service.yaml

build_mlflow:
	${KUBERNETES_CLIENT} apply -f minikube/deployments/mlflow_deployment.yaml
	${KUBERNETES_CLIENT} apply -f minikube/services/mlflow_service.yaml

build_knative:
	${KUBERNETES_CLIENT} apply -f minikube/deployments/knative_deployment.yaml

clean:
	${KUBERNETES_CLIENT} delete -f minikube/configmap/project_config.yaml
	${KUBERNETES_CLIENT} delete -f minikube/volumes/minio_volume.yaml
	${KUBERNETES_CLIENT} delete -f minikube/deployments/minio_deployment.yaml
	${KUBERNETES_CLIENT} delete -f minikube/services/minio_service.yaml
	${KUBERNETES_CLIENT} delete -f minikube/volumes/postgres_volume.yaml
	${KUBERNETES_CLIENT} delete -f minikube/deployments/postgres_deployment.yaml
	${KUBERNETES_CLIENT} delete -f minikube/services/postgres_service.yaml
	${KUBERNETES_CLIENT} delete -f minikube/deployments/mlflow_deployment.yaml
	${KUBERNETES_CLIENT} delete -f minikube/services/mlflow_service.yaml
	${KUBERNETES_CLIENT} delete -f minikube/deployments/knative_deployment.yaml
