#!/usr/bin/env bash -v

set -o errexit
set -o nounset
set -o pipefail

docker build -t jguionne/index_server:latest -f Dockerfile.index .
docker build -t jguionne/flask_demo:latest -f Dockerfile.flask .
docker build -t jguionne/all_demo:latest -f Dockerfile.all2 .

docker push jguionne/index_server:latest
docker push jguionne/flask_demo:latest
docker push jguionne/all_demo:latest

#docker run -e OPENAI_API_KEY=$OPENAI_API_KEY jguionne/index_server:latest 
#docker run -p 5001:5001 jguionne/flask_demo:latest 
#docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 5001:5001 jguionne/all_demo:latest