import os
import pickle

# NOTE: for local testing only, do NOT deploy with your key hardcoded
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# os.environ['OPENAI_API_KEY'] = "your key here"

from multiprocessing import Lock
from multiprocessing.managers import BaseManager
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, Document, ServiceContext, StorageContext, load_index_from_storage

index = None
stored_docs = {}
lock = Lock()

# VOLUME_ROOT = "/app/data"
VOLUME_ROOT = os.environ.get("VOLUME_ROOT")
INDEX_DIRECTORY = VOLUME_ROOT + "/saved_index"
PICKLE_DB =  VOLUME_ROOT +"/stored_documents.pkl"


def initialize_index():
    """Create a new global index, or load one from the pre-set path."""
    global index, stored_docs

    print("initializing index...")
    
    service_context = ServiceContext.from_defaults(chunk_size_limit=512)
    with lock:
        if os.path.exists(INDEX_DIRECTORY):
            index = load_index_from_storage(StorageContext.from_defaults(persist_dir=INDEX_DIRECTORY), service_context=service_context)
        else:
            index = GPTVectorStoreIndex([], service_context=service_context)
            index.storage_context.persist(persist_dir=INDEX_DIRECTORY)
        if os.path.exists(PICKLE_DB):
            with open(PICKLE_DB, "rb") as f:
                stored_docs = pickle.load(f)


def query_index(query_text):
    """Query the global index."""
    global index
    print("querying index..." + query_text)
    response = index.as_query_engine().query(query_text)
    return response


def insert_into_index(doc_file_path, doc_id=None):
    """Insert new document into global index."""

    print("inserting into index..." + doc_file_path)    
    global index, stored_docs
    document = SimpleDirectoryReader(input_files=[doc_file_path]).load_data()[0]
    if doc_id is not None:
        document.doc_id = doc_id

    with lock:
        # Keep track of stored docs -- llama_index doesn't make this easy
        stored_docs[document.doc_id] = document.text[0:200]  # only take the first 200 chars

        index.insert(document)
        index.storage_context.persist(persist_dir=INDEX_DIRECTORY)
        
        with open(PICKLE_DB, "wb") as f:
            pickle.dump(stored_docs, f)

    return

def get_documents_list():
    """Get the list of currently stored documents."""
    global stored_doc
    print("getting documents list...")
    documents_list = []
    for doc_id, doc_text in stored_docs.items():
        documents_list.append({"id": doc_id, "text": doc_text})

    return documents_list


if __name__ == "__main__":
    # init the global index
    print("initializing index..." + VOLUME_ROOT + " " + INDEX_DIRECTORY + " " + PICKLE_DB)
    initialize_index()

    # setup server
    # NOTE: you might want to handle the password in a less hardcoded way
    manager = BaseManager(('', 5602), b'password')
    manager.register('query_index', query_index)
    manager.register('insert_into_index', insert_into_index)
    manager.register('get_documents_list', get_documents_list)
    server = manager.get_server()

    print("server started...")
    server.serve_forever()
