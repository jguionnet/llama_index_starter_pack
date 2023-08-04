import os
from multiprocessing.managers import BaseManager
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

VOLUME_ROOT = os.environ.get("VOLUME_ROOT")
UPLOAD_FOLDER = VOLUME_ROOT + '/uploads'


# initialize manager connection
# NOTE: you might want to handle the password in a less hardcoded way
manager = BaseManager(('0.0.0.0', 5602), b'password')
manager.register('query_index')
manager.register('insert_into_index')
manager.register('get_documents_list')
manager.connect()

@app.route("/query", methods=["GET"])
def query_index():
    global manager
    query_text = request.args.get("text", None)
    if query_text is None:
        return "No text found, please include a ?text=blah parameter in the URL", 400
    
    response = manager.query_index(query_text)._getvalue()
    response_json = {
        "text": str(response),
        "sources": [{"text": str(x.source_text), 
                     "similarity": round(x.similarity, 2),
                     "doc_id": str(x.doc_id),
                     "start": x.node_info['start'],
                     "end": x.node_info['end']
                    } for x in response.source_nodes]
    }
    return make_response(jsonify(response_json)), 200


@app.route('/upload/test', methods=['POST'])
def file_upload():
    file = request.files['file']
    filename = file.filename
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return {"message": f"The file '{filename}' has been successfully uploaded."}, 200


@app.route("/upload", methods=["POST"])
def upload_file():
    global manager
    if 'file' not in request.files:
        return "Please send a POST request with a file", 400
    filepath = None
    try: 
        file = request.files["file"]
        filename = file.filename
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        manager.insert_into_index(filepath, doc_id=filename )

    except Exception as e:
        # cleanup temp file
        if filepath is not None and os.path.exists(filepath):
            os.remove(filepath)
        return "Error: {}".format(str(e)), 500

    return {"message": f"The file '{filename}' has been successfully indexed."}, 200


@app.route("/getDocuments", methods=["GET"])
def get_documents():
    document_list = manager.get_documents_list()._getvalue()
    return make_response(jsonify(document_list)), 200
    

@app.route("/")
def home():
    return "Hello, World! Welcome to the llama_index docker image!"


if __name__ == "__main__":
    print('Starting Flask REST API server...')
    app.run(debug=True, host="0.0.0.0", port=5001)
