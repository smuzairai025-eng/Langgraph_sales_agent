import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import TypedDict
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

faiss_path=os.getenv('Faiss_path')
file_path=os.getenv('DATA_DIR')

def document_loader(filepath : str)->str:
    with open(filepath,'r',encoding='utf-8') as file:
        content=file.read()
    return content

def text_splitter(doc : list[str]):
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=80)
    return splitter.split_documents(doc)

def get_retriever():
    embeddings=OpenAIEmbeddings(model='text-embedding-3-small')

    if os.path.exists(faiss_path):
        print("Loading existing FAISS Vectorstore")
        vector_store=FAISS.load_local(folder_path=faiss_path, embeddings=embeddings,
                                      allow_dangerous_deserialization=True)
        return vector_store.as_retriever(kwargs={'k':3})
    else:
        loaded_doc=document_loader(file_path)
        doc_obj=Document(page_content=loaded_doc)
        chunks=text_splitter([doc_obj])
        
        print("Creating new faiss vector store")
        vector_store=FAISS.from_documents(documents=chunks, embedding=embeddings)
        vector_store.save_local(faiss_path,'vectors_index')
        return vector_store.as_retriever(kwargs={'k':3})