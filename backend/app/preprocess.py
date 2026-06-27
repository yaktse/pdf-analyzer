# Preprocess stuff
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from app.global_vars import *
from pathlib import Path

class Preprocessor:
    def __init__(self):
        # NOTE: Heavy on CPU
        # self.embeddings = HuggingFaceEmbeddings(
            # model_name="BAAI/bge-m3",
            # model_kwargs={
                # "device": "cpu"
            # },
            # encode_kwargs={
                # "normalize_embeddings": True
            # }
        # )

        # Very low CPU usage
        self.embeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=10,
        )

        self.vectorstore = Chroma(
            collection_name="documents",
            persist_directory="./chroma_db",
            embedding_function=self.embeddings,
        )


    def injest(self, metadata: str, corpus: str):
        pass

    async def injest_pdf(self, metadata, filename):
        """
        All data from user is saved into _context folder, and `filename` assumes 
        is as current directory.
        """

        loader = PyPDFLoader(CONTEXT_DIR / filename)
        documents = loader.load()
        chunks = self.splitter.split_documents(documents)
        self.vectorstore.add_documents(chunks)

        print(doc.metadata)
