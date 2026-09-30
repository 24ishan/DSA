# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
# from langchain_postgres.vectorstores import PGVector
# from app.config import DATABASE_URL
#
# COLLECTION_NAME = "medical_knowledge"
# PDF_PATH = "data/tachycardia_1.pdf"
#
#
# def ingest_medical_data():
#     loader = PyPDFLoader(PDF_PATH)
#     docs = loader.load()[:10]
#
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
#     chunks = text_splitter.split_documents(docs)
#
#     # Talk to the PC (Ollama)
#     embeddings = OllamaEmbeddings(model="llama3")
#
#     print(f"💾 Storing {len(chunks)} chunks using the new PGVector library...")
#
#     # NEW SYNTAX for langchain-postgres
#     vector_store = PGVector.from_documents(
#         embedding=embeddings,
#         documents=chunks,
#         collection_name=COLLECTION_NAME,
#         connection=DATABASE_URL,  # Key change: 'connection' instead of 'connection_string'
#         use_jsonb=True,
#     )
#     print("✅ Ingestion complete!")
#
#
# if __name__ == "__main__":
#     ingest_medical_data()
        ###############################################################################################################
# import os
# import hashlib
# import json
# from typing import List, Dict
# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document
# from app import setup_logging
#
# logger = setup_logging()
# os.environ["OLLAMA_HOST"] = "http://192.168.1.2:11434"
# os.environ["NO_PROXY"] = "localhost,127.0.0.1,192.168.1.2"
#
# class RAGIndexer:
#     def __init__(self, index_path: str = "faiss_index", registry_path: str = "fingerprints.json"):
#         self.index_path = index_path
#         self.registry_path = registry_path
#         self.embeddings = OllamaEmbeddings(model="llama3",base_url="http://192.168.1.2:11434")
#         self.fingerprints = self._load_registry()
#         self.vector_db = self._load_vector_db()
#
#     def _load_registry(self) -> Dict:
#         """Loads the record of already processed file hashes."""
#         if os.path.exists(self.registry_path):
#             with open(self.registry_path, 'r') as f:
#                 return json.load(f)
#         return {}
#
#     def _save_registry(self):
#         with open(self.registry_path, 'w') as f:
#             json.dump(self.fingerprints, f)
#
#     def _load_vector_db(self):
#         """Loads existing FAISS index or returns None."""
#         if os.path.exists(self.index_path):
#             return FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
#         return None
#
#     def get_file_hash(self, file_path: str) -> str:
#         """PDF Fingerprinting: Generates a SHA-256 hash of the file content."""
#         hasher = hashlib.sha256()
#         with open(file_path, "rb") as f:
#             while chunk := f.read(8192):
#                 hasher.update(chunk)
#         return hasher.hexdigest()
#
#     def process_document(self, file_path: str):
#         file_name = os.path.basename(file_path)
#         file_hash = self.get_file_hash(file_path)
#
#         # 1. Check Fingerprint for Deduplication
#         if file_hash in self.fingerprints.values():
#             logger.info(f"Skipping '{file_name}': Fingerprint already exists in index.")
#             return
#
#         logger.info(f"Processing new document: {file_name}")
#
#         try:
#             # 2. Page Indexing (Loading)
#             loader = PyPDFLoader(file_path)
#             pages = loader.load()[:10]
#
#             # 3. Recursive Chunking (Preserving Context)
#             text_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=1000,
#                 chunk_overlap=150,
#                 length_function=len,
#                 add_start_index=True
#             )
#
#             # Enrich metadata before adding to Vector DB
#             final_chunks = []
#             for chunk in text_splitter.split_documents(pages):
#                 chunk.metadata.update({
#                     "file_hash": file_hash,
#                     "source": file_name,
#                     "processed_at": "2026-03-03"
#                 })
#                 final_chunks.append(chunk)
#
#             # 4. Upsert to Vector Database
#             if self.vector_db is None:
#                 self.vector_db = FAISS.from_documents(final_chunks, self.embeddings)
#             else:
#                 self.vector_db.add_documents(final_chunks)
#
#             # 5. Update Registry & Save State
#             self.fingerprints[file_name] = file_hash
#             self.vector_db.save_local(self.index_path)
#             self._save_registry()
#
#             logger.info(f"Successfully indexed {len(final_chunks)} chunks from {file_name}.")
#
#         except Exception as e:
#             logger.error(f"Failed to process {file_name}: {str(e)}")
#
#
# # --- Execution ---
# if __name__ == "__main__":
#     import os
#     from dotenv import load_dotenv
#
#     load_dotenv()
#
#     # # Print all env vars in a readable list
#     # print("--- ACTIVE ENVIRONMENT VARIABLES ---")
#     # for key, value in os.environ.items():
#     #     print(f"{key}: {value}")
#     # print("-----------------------------------")
#     indexer = RAGIndexer()
#
#     # Simulate processing a document
#     indexer.process_document("data/tachycardia_1.pdf")
#
#     print("Indexer initialized. Ready for production ingest.")


    #################################################################################################################