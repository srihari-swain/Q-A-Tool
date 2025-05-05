# Web Content Q&A Tool

A Python-based application that scrapes webpage content, creates embeddings, and answers questions based on the ingested information using a Retrieval-Augmented Generation (RAG) pipeline powered by Groq.

## 📺 Demo

Check out the demo video to see the tool in action:

[![Web Content Q&A Tool Demo](https://img.youtube.com/vi/Dt6UrN-Nc7A/0.jpg)](https://www.youtube.com/watch?v=Dt6UrN-Nc7A)

## 🚀 Features

- **Web Scraping** – Scrape main content from one or more webpage URLs using BeautifulSoup and Playwright
- **Embeddings + Vector Store** – Convert content to embeddings using HuggingFace's all-MiniLM-L6-v2 model and store in FAISS
- **RAG-based Q&A** – Uses LangChain with Groq LLMs to answer questions based only on ingested content

## 🧠 Technical Stack

| Component | Technology Used |
|-----------|----------------|
| Web Scraping | BeautifulSoup4 + Playwright |
| Embedding Model | all-MiniLM-L6-v2 (via HuggingFace) |
| Vector Database | FAISS |
| RAG Framework | LangChain + LangChain Community |
| LLM API | Groq (langchain-groq) |
| UI | Streamlit |

## 📦 Installation & Setup

Follow these steps to install and run the application:

### 1. Create a Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Clone the Repository

```bash
git clone https://github.com/srihari-swain/Q-A-Tool.git
cd Q-A-Tool
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Playwright

```bash
playwright install
```

### 5. Configure Groq API Key

Create a `.env` file in the project root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can get your API key by signing up at [Groq Cloud](https://console.groq.com/).



## 🚀 Running the Application

```bash
streamlit run main.py
```

The application will be available at http://localhost:8501 in your web browser.

## 🎬 How It Works

1. **URL Ingestion**: The tool scrapes content from the provided URLs using BeautifulSoup and Playwright to handle JavaScript-rendered websites.
2. **Text Processing**: The extracted content is cleaned and split into manageable chunks using LangChain's RecursiveCharacterTextSplitter.
3. **Embedding Creation**: Using the Sentence Transformer model, each text chunk is converted into numerical vector representations.
4. **Vector Storage**: These embeddings are stored in a FAISS vector database for efficient similarity search.
5. **Question Processing**: When you ask a question, it's also converted to an embedding.
6. **Retrieval**: The system finds the most relevant content chunks by comparing your question embedding with stored content embeddings.
7. **Answer Generation**: The relevant chunks and your question are sent to Groq's LLM to generate a contextually accurate answer.
