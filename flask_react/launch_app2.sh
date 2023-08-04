#!/bin/bash -x


export VOLUME_ROOT=/Users/jguionnet/workspace/llama_index_starter_pack/flask_react/volume
export API_BASE_URL="http://127.0.0.1:5001"

# start backend index server
python ./index_server.py &
echo "index_server running..."

# wait for the server to start - if creating a brand new huge index, on startup, increase this further
sleep 15

# start the flask server
python ./rest_api_server.py &
echo "flask demo done..."

streamlit run streamlit_ui.py