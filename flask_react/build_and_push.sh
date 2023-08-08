#!/usr/bin/env bash -v

# set -o errexit
# set -o nounset
# set -o pipefail

# docker build -t jguionne/index_server:latest -f Dockerfile.index .
# docker build -t jguionne/rest_api_server:latest -f Dockerfile.rest_api .
docker build -t jguionne/streamlit_ui:latest -f Dockerfile.ui .

# docker push jguionne/index_server:latest
# docker push jguionne/rest_api_server:latest
docker push jguionne/streamlit_ui:latest 

#docker run -e OPENAI_API_KEY=$OPENAI_API_KEY jguionne/index_server:latest 
#docker run -p 5001:5001 jguionne/rest_api_server:latest 
#docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 5001:5001 jguionne/all_demo:latest

kubectl delete -f k8s/deployment.yml # Index and query server layer 
kubectl apply -f k8s/deployment.yml # Index and query server layer 
kubectl delete -f k8s/deployment_ui.yml # Index and query server layer 
kubectl apply -f k8s/deployment_ui.yml # Index and query server layer 
# kubectl apply -f k8s/deployment_api.yml # Flask/Rest layer
kubectl apply -f k8s/external-secrets.yml # API Key
# kubectl apply -f k8s/gateway_config_api.yml # API layer ingress
kubectl apply -f k8s/gateway_config.yml # Index and query layer ingress
kubectl apply -f k8s/gateway_config_ui.yml # Index and query layer ingress
# kubectl apply -f k8s/jobq.yaml
kubectl apply -f k8s/volume.yml