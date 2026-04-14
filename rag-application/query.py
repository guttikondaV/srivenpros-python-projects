import langchain_openai as lc_oa
import langchain_core.prompts as prompts
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage

chat_history = []


def ask_and_get_answer(vector_store, query, k=3):
    llm = lc_oa.ChatOpenAI(model='gpt-3.5-turbo', temperature=0.0)

    retriever = vector_store.as_retriever(search_type='similarity',
                                          search_kwargs={'k': k})

    # Define a prompt template for better control
    prompt = prompts.ChatPromptTemplate.from_template("""
        Answer the following question based only on the provided context:
        <context>
        {context}
        </context>
        Question: {input}""")

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({"input": query})
    return response


def ask_question(query, chain):
    response = chain.invoke({
        "input": query,
        "chat_history": chat_history
    })

    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response["answer"]))

    return response
