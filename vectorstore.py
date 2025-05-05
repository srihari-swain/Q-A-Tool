import logging

from scrapper import scrape_url
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestUrls:
    def __init__(self):
        self.sources = {}
        self.vector_store = None
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {e}")
            raise
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )

    def process(self, urls):
        """Ingest content from multiple URLs into the vector store."""
        all_texts = []
        url_mapping = {}  
        
        for url in urls:
            try:
                content = scrape_url(url)
                if not content or content.startswith("Error scraping"):
                    logger.warning(f"Skipping URL due to scraping error: {url}")
                    continue
                chunks = self.text_splitter.split_text(content)
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{url}_{i}"
                    url_mapping[chunk_id] = url
                    all_texts.append(f"Source: {chunk_id}\n\n{chunk}")
                    self.sources[chunk_id] = url
            except Exception as e:
                logger.error(f"Error processing URL {url}: {e}")
                continue
        
        if not all_texts:
            logger.warning("No content was successfully ingested.")
            return None, self.sources

        try:
            if self.vector_store is None:
                self.vector_store = FAISS.from_texts(all_texts, self.embeddings)
            else:
                temp_db = FAISS.from_texts(all_texts, self.embeddings)
                self.vector_store.merge_from(temp_db)
        except Exception as e:
            logger.error(f"Error creating or merging FAISS vector store: {e}")
            raise
        
        return self.vector_store, self.sources
