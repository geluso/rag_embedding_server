from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from document_payload import DocumentPayload

embeddings = HuggingFaceEmbeddings(model_name="nlpaueb/legal-bert-base-uncased")
persist_directory = "./chroma_db"
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory
)

def remove_docs_without_parent_id():
    docs = vectorstore.get()
    ids = []
    for meta in docs['metadatas']:
        if not "parent_id" in meta:
            doc_id = meta['id']
            ids.append(doc_id)

    print(len(ids))
    vectorstore.delete(ids=ids)

def hash_docs_and_delete_dupes():
    docs = vectorstore.get()
    ids = []
    hash_to_doc_ids = {}
    for (doc_id, text) in zip(docs['ids'], docs['documents']):
        text_hash = hash(text)
        if text_hash not in hash_to_doc_ids:
            hash_to_doc_ids[text_hash] = []
        hash_to_doc_ids[text_hash].append(doc_id)

    occurences = {}
    for doc_hash in hash_to_doc_ids.keys():
        doc_count = len(hash_to_doc_ids[doc_hash])
        if doc_count not in occurences:
            occurences[doc_count] = 0
        occurences[doc_count] = occurences[doc_count] + 1
    print(occurences)

    # for doc_hash in hash_to_doc_ids.keys():
    #     ids = hash_to_doc_ids[doc_hash]
    #     doc_count = len(ids)
    #     if doc_count > 1:
    #         ids_to_delete = ids[1:]
    #         vectorstore.delete(ids=ids_to_delete)


hash_docs_and_delete_dupes()
