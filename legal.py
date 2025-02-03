import sys
import numpy as np

from uuid import uuid4
from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="nlpaueb/legal-bert-base-uncased")

from langchain_chroma import Chroma

persist_directory = "./chroma_db_legal"
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory
)

docs = [
  Document(page_content="I will sue you.", id=str(uuid4())),
  Document(page_content="You are out of order", id=str(uuid4())),
  Document(page_content="I move to strike that from the record", id=str(uuid4())),
  Document(page_content="Objection your honor", id=str(uuid4())),
  Document(page_content="If the glove don't fit you must acquit", id=str(uuid4())),
  Document(page_content="If the word2vec don't fit you must acquit", id=str(uuid4())),
  Document(page_content="Two cheeseburgers, please.", id=str(uuid4())),
  Document(page_content="Lady killer", id=str(uuid4())),
  Document(page_content="Murder", id=str(uuid4())),
  Document(page_content="NFL", id=str(uuid4())),
  Document(page_content="LA riots", id=str(uuid4())),
]

vectorstore.add_documents(documents=docs, ids=[doc.id for doc in docs])
results = vectorstore.similarity_search_with_score("OJ simpson")

for doc, score in results:
  print(score, doc.page_content)