from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGTemplate:
    def __init__(self, config):
        self.config = config
        self.embeddings = OpenAIEmbeddings(api_key=config["api_key"])
    
    def create_vector_store(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config["chunk_size"]
        )
        chunks = splitter.split_documents(documents)
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        vector_store.save_local(self.config["vector_db_path"])
        return vector_store
    
    def retrieve_context(self, query, k=5):
        try:
            vector_store = FAISS.load_local(
                self.config["vector_db_path"],
                self.embeddings
            )
            return vector_store.similarity_search(query, k=k)
        except:
            return []
