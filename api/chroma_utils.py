from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,UnstructuredHTMLLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os


embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
vectorstore = Chroma(persist_directory="./chroma_db",embedding_function=embedding_function,)


def load_and_split_document(file_path: str) -> List[Document]:
    if not os.path.isfile(file_path):
        print(f"File not found at: {file_path}")
        return []

    # Select appropriate loader based on file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_extension == '.docx':
        loader = Docx2txtLoader(file_path)
    elif file_extension == '.txt':
        loader = TextLoader(file_path, encoding='utf-8')
    elif file_extension == '.html':
        loader = UnstructuredHTMLLoader(file_path)
    else:
        print(f"Unsupported format: {file_path}")
        return []

    try:
        documents = loader.load()
    except Exception as e:
        print(f"Error loading document: {e}")
        return []

    # Optional: Apply text splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    return text_splitter.split_documents(documents)

def index_document_to_chroma(file_path:str,file_id:int)->bool:
    try:
        splits=load_and_split_document(file_path)
        for split in splits:
            split.metadata['file_id']=file_id
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document:{e}")
        return False
    

def delete_doc_from_chroma(file_id:int):
    try:
        docs=vectorstore.get(where={"file_id":file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        vectorstore._collection.delete(where={"file_id":file_id})
        print(f"Deleted all documents with file_id {file_id}")
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma:{str(e)}")
        return False