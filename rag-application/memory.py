from langchain_openai import ChatOpenAI
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def build_rag_chain(vector_store, k=5):
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    retriever = vector_store.as_retriever(
        search_type='similarity',
        search_kwargs={'k': k}
    )

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, just "
        "reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = (
        "You are an assistant for question-answering tasks. Use "
        "the following pieces of retrieved context to answer the "
        "question. If you don't know the answer, just say that you "
        "don't know. Use three sentences maximum and keep the answer "
        "concise."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    question_answer_chain = create_stuff_documents_chain(
        llm, qa_prompt
    )

    rag_chain = create_retrieval_chain(history_aware_retriever,
                                       question_answer_chain)
    return rag_chain
