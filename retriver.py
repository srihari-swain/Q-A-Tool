import os
import re
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

class Retriever:
    def __init__(self, vector_store, sources, api_key , provider="groq", model_name=None):
        """
        Args:
            vector_store: Your vector DB or FAISS/Chroma instance.
            sources: Dict mapping source IDs to URLs.
            provider: "openai", "ollama", or "groq".
            model_name: Model name for the provider.
        """
        self.vector_store = vector_store
        self.sources = sources
        self.k = 4

        try:
            api_key = api_key
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables.")

            model_name = model_name or "llama3-8b-8192"
            try:
                self.llm = ChatGroq(model=model_name, api_key=api_key)
            except Exception as e:
                raise RuntimeError(f"Groq model initialization failed: {e}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {e}")

        self.prompt_template = """
        "Hello! I am your helpful assistant.\n\n"
        "Hi there! I'm here to assist you with your question.\n"
        "Greetings! Let's find the information you're looking for.\n"
        "Welcome! I'm ready to help based on the content provided.\n\n"

        You are a helpful assistant that answers questions strictly based on the retrieved content.

        Retrieved content:
        {context}

        Question: {question}

        Important instructions:
        1. Answer only using information from the retrieved content.
        2. If the answer cannot be found in the retrieved content, say "I cannot answer this based on the provided web content."
        3. Do not use any external knowledge or make assumptions.
        4. Cite the source URLs in your answer.

        Answer:
        """
        try:
            self.PROMPT = PromptTemplate(
                template=self.prompt_template,
                input_variables=["context", "question"]
            )
            if not hasattr(self.vector_store, "as_retriever"):
                raise ValueError("Provided vector_store does not have 'as_retriever' method.")
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": self.k}),
                chain_type_kwargs={"prompt": self.PROMPT},
                return_source_documents=True
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize QA chain: {e}")

    def answer_question(self, question, k=4):
        """Answer a question using the ingested content."""
        if not self.vector_store:
            return "Error: Please ingest some URLs first."
        if not question or not isinstance(question, str):
            return "Error: Question must be a non-empty string."
        try:
            result = self.qa_chain.invoke({"query": question})
            source_docs = result.get("source_documents", [])
            unique_sources = set()

            for doc in source_docs:
                content = getattr(doc, "page_content", "")
                source_match = re.search(r"Source: ([^\n]+)", content)
                if source_match:
                    source_id = source_match.group(1).strip()
                    if source_id in self.sources:
                        unique_sources.add(self.sources[source_id])

            answer = result.get("result", "No answer generated.")
            if unique_sources and "Source" not in answer:
                sources_text = "\n\nSources:\n" + "\n".join(unique_sources)
                answer += sources_text

            return answer
        except Exception as e:
            return f"Error during question answering: {e}"
