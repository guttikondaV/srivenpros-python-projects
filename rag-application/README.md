# RAG Application

A Retrieval-Augmented Generation (RAG) application built with LangChain, OpenAI,
and ChromaDB. Load documents, embed them into a persistent vector store, and ask
questions with full conversation memory.

## Features

- **Multi-format document loading** — supports PDF, TXT, and DOCX files
- **Automatic chunking** — splits documents into overlapping chunks for better
  retrieval
- **Persistent vector store** — embeddings are saved to disk via ChromaDB and
  reloaded between runs
- **Conversation memory** — a history-aware retriever reformulates follow-up
  questions so context carries across turns
- **Interactive CLI** — ask questions in a loop; type `exit`, `quit`, or `bye`
  to stop

## Project Structure

```
rag-application/
├── main.py       # Entry point — orchestrates loading, embedding, and the Q&A loop
├── io.py         # Document loading and text chunking
├── db.py         # Embedding creation and ChromaDB persistence
├── memory.py     # History-aware RAG chain construction
└── query.py      # Single-turn and multi-turn question answering
```

## Setup

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- An OpenAI API key

### Install dependencies

```bash
uv sync
```

### Configure environment

Create a `.env` file in the project root (or the `rag-application/` directory):

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

Place any PDF, TXT, or DOCX file inside a `files/` directory, update the path in
`main.py`, then run:

```bash
uv run -m rag-application
```

Or if running directly:

```bash
python -m rag-application
```

The application will:

1. Load and chunk the document
2. Generate embeddings and persist them to `./chroma_db/`
3. Load the vector store and build a history-aware RAG chain
4. Start an interactive Q&A loop

```
Your question: What is the main topic of this document?
...
Your question: Can you elaborate on that?
...
Your question: exit
Bye bye!
```

## Models Used

| Component  | Model                    |
|------------|--------------------------|
| Embeddings | `text-embedding-3-small` |
| Chat LLM   | `gpt-3.5-turbo`          |

## Dependencies

- [LangChain](https://github.com/langchain-ai/langchain)
- [langchain-openai](https://github.com/langchain-ai/langchain/tree/master/libs/partners/openai)
- [langchain-chroma](https://github.com/langchain-ai/langchain/tree/master/libs/partners/chroma)
- [ChromaDB](https://www.trychroma.com/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
