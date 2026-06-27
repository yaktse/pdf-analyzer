# Preprocess stuff

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)

class Preprocessor:
    def __init__(self):
        pass

    def injest(metadata: str, corpus: str):
        pass

    def injest_pdf(path_to_file):
        """
        All data from user is saved into _context folder, and `path_to_file` assumes 
        is as current directory.
        """

        loader = PyPDFLoader("_context/" + path_to_file)
        doc = loader.load()[0]
        print(doc.metadata)
