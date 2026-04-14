import os
import dotenv

from . import io as app_io
from . import db
from . import query
from . import memory


def main():
    # Step 1: Load env files so that secrets aren't commmited to github
    dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

    # Step 2: Read Document, Chunk it and create embeddings
    data = app_io.load_file(
        'files/rag_powered_by_google_search.pdf')  # use any file you have

    chunks = app_io.chunk_data(data, chunk_size=256)

    vector_store = db.create_embeddings_chroma(chunks)

    # Step 3: Load existing embeddings and build RAG chain
    loaded_store = db.load_embeddings_chroma()
    rag_chain = memory.build_rag_chain(loaded_store)

    q = 'How many pairs of questions and answers had the StackOverflow dataset?'

    answer = query.ask_and_get_answer(vector_store, q)
    print(answer)

    user_query = 'Multiply the answer by 4.'

    result = query.ask_question(user_query, rag_chain)

    print(result['answer'])

    # Interactive Workflow
    while True:
        user_query = input('Your question: ')
        if user_query.lower() in ['exit', 'quit', 'bye']:
            print('Bye bye!')
            break
        result = query.ask_question(user_query, rag_chain)
        print(result['answer'])
        print('-' * 100)


if __name__ == '__main__':
    main()
