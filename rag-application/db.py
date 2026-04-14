import langchain_chroma as lc_ch
import langchain_openai as lc_oa


def create_embeddings_chroma(chunks, persist_directory='./chroma_db'):
    embeddings = lc_oa.OpenAIEmbeddings(model='text-embedding-3-small',
                                        dimensions=1536)

    vector_store = lc_ch.Chroma.from_documents(chunks, embeddings,
                                               persist_directory=persist_directory)

    return vector_store


def load_embeddings_chroma(persist_directory='./chroma_db'):
    embeddings = lc_oa.OpenAIEmbeddings(model='text-embedding-3-small',
                                        dimensions=1536)

    vector_store = lc_ch.Chroma(persist_directory=persist_directory,
                                embedding_function=embeddings)

    return vector_store
