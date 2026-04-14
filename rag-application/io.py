import os

import langchain_text_splitters as text_splitters
import langchain_community.document_loaders as doc_loaders


def load_file(file):
    _, extension = os.path.splitext(file)

    loaders = {
        ".pdf": doc_loaders.PyPDFLoader,
        '.txt': doc_loaders.TextLoader,
        ".docx": doc_loaders.Docx2txtLoader,
    }

    if extension not in loaders:
        raise Exception("Invalid file extension or file type not supported yet")

    loader = loaders[extension]

    data = loader(file).load()
    return data


def chunk_data(data, chunk_size: int = 256):
    overlap = int(chunk_size * 0.15)

    text_splitter = text_splitters.RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )

    chunks = text_splitter.split_documents(data)

    return chunks
