from uuid import uuid4
from flask import Flask, request, jsonify

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from document_payload import DocumentPayload

from db import create_default_connection, create_text_embedding_metadata, find_one_text_embedding_metadata, find_one_text_embedding_metadata_by_id, add_summary

embeddings = HuggingFaceEmbeddings(model_name="nlpaueb/legal-bert-base-uncased")
persist_directory = "./chroma_db"
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory
)

app = Flask(__name__)

def get_label(lang_doc):
    if "title" in lang_doc.metadata:
        return lang_doc.metadata['title']
    if "label" in lang_doc.metadata:
        return lang_doc.metadata['label']
    return ""

def get_url(lang_doc):
    if "url" in lang_doc.metadata:
        return lang_doc.metadata['url']
    if "source" in lang_doc.metadata:
        return lang_doc.metadata['source']
    return ""

@app.route("/search/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = vectorstore.similarity_search_with_score(query)
    print(len(results), "results")
    for result in results:
        print(result)
    response = []
    for lang_doc, score in results:
        title = get_label(lang_doc)
        url = get_url(lang_doc)
        text = lang_doc.page_content
        doc = DocumentPayload(title, url, text)
        response.append({
            "score": float(score),
            "doc": doc.to_dict()
        })
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
