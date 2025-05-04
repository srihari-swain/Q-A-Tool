# Web Content Q&A Tool

A Python-based application that scrapes webpage content, creates embeddings, and answers questions based on the ingested information using a Retrieval-Augmented Generation (RAG) pipeline.

## 📺 Demo

Check out the demo video to see the tool in action:

[![Web Content Q&A Tool Demo](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=Dt6UrN-Nc7A)



## 🚀 Features

- **Web Scraping** – Scrape main content from one or more webpage URLs.
- **Embeddings + Vector Store** – Convert content to embeddings using HuggingFace models and store in FAISS.
- **RAG-based Q&A** – Uses LangChain with your choice of OpenAI, Groq, or Ollama LLMs to answer questions based only on ingested content.

## 🧠 Technical Stack

| Component | Technology Used |
|-----------|----------------|
| Web Scraping | BeautifulSoup4 + Playwright |
| Embedding Model | all-MiniLM-L6-v2 (via HuggingFace) |
| Vector Database | FAISS |
| RAG Framework | LangChain + LangChain Community |
| LLM API | OpenAI (langchain-openai)<br>Groq (langchain[groq])<br>Ollama (langchain-ollama) |

## 📦 Installation & Running the App

Follow these steps to install and run the application with your preferred LLM backend:

### 1. Clone the Repository

```bash
git clone https://github.com/srihari-swain/Al-ML-projects.git
```

### 2. Go to the Main Directory

```bash
cd web-content-qa
```

### 3. Install the Required Dependencies

Install the core dependencies:

```bash
pip install -r requirements.txt

```
Initialize Playwright

```bash
playwright install 

```

Then, install one or more LLM integrations depending on your use case:

**OpenAI:**
```bash
pip install langchain-openai
```

**Groq:**
```bash
pip install "langchain[groq]"
```

**Ollama:**
```bash
pip install langchain-ollama
```

### 4. Set Up Your LLM Provider

**OpenAI:**
- Get your API key from OpenAI dashboard.
- Set it as an environment variable or in a .env file:
  ```
  OPENAI_API_KEY=sk-...
  ```

**Groq:**
- Get your API key from Groq Cloud.
- Set it as an environment variable or in a .env file:
  ```
  GROQ_API_KEY=...
  ```

**Ollama:**
- Install Ollama and run:
  ```bash
  ollama serve
  ollama pull llama3.1
  ```

### 5. Configure the Retriever

In your code, you can select the retriever type by initializing the appropriate class:
- OpenAI: `from langchain_openai import ChatOpenAI`
- Groq: `from langchain.chat_models import init_chat_model`
- Ollama: `from langchain_ollama.chat_models import ChatOllama`

Your app can be set up to auto-select based on which API key is present or which service is running.

### 6. Run the Main Script

```bash
streamlit run main.py
```

## 🧩 Retriever Options

You can use any of the following retrievers in your pipeline:

| Retriever | Dependency | How to Use in Code Example |
|-----------|------------|----------------------------|
| OpenAI | langchain-openai | `llm = ChatOpenAI(model="gpt-4o", temperature=0)` |
| Groq | langchain[groq] | `llm = init_chat_model("llama3-8b-8192", model_provider="groq")` |
| Ollama | langchain-ollama | `llm = ChatOllama(model="llama3.1", temperature=0)` |

## 🎬 How It Works

The application follows these steps to provide answers based on web content:

1. **URL Ingestion**: The tool scrapes content from the provided URLs using BeautifulSoup and Playwright to handle JavaScript-rendered websites.
2. **Text Processing**: The extracted content is cleaned and split into manageable chunks.
3. **Embedding Creation**: Using the Sentence Transformer model, each text chunk is converted into numerical vector representations.
4. **Vector Storage**: These embeddings are stored in a FAISS vector database for efficient similarity search.
5. **Question Processing**: When you ask a question, it's also converted to an embedding.
6. **Retrieval**: The system finds the most relevant content chunks by comparing your question embedding with stored content embeddings.
7. **Answer Generation**: The relevant chunks and your question are sent to the LLM to generate a contextually accurate answer.