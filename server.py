from uuid import uuid4
from flask import Flask, request, jsonify

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from document_payload import DocumentPayload

from db import create_default_connection, create_text_embedding_metadata, find_one_text_embedding_metadata

embeddings = HuggingFaceEmbeddings(model_name="nlpaueb/legal-bert-base-uncased")
persist_directory = "./chroma_db"
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory=persist_directory
)

app = Flask(__name__)

@app.route("/metadata/", methods=["GET"])
def get_metadata():
    label = request.args.get('label')
    row_id, parent_id, datatype, label, summary = find_one_text_embedding_metadata(label)
    return jsonify({"rowId": row_id, "parentId": parent_id, "datatype": datatype, "label": label, "summary": summary})

# parent_id, datatype, label, summary) VALUES (%s, %s, %s, %s)",
@app.route("/metadata/", methods=["POST"])
def create_metadata():
    data = request.json
    parent_id = data.get("parentId", "")
    datatype = data.get("datatype", "")
    label = data.get("label", "")
    summary = ''

    conn = create_default_connection()
    create_text_embedding_metadata(parent_id, datatype, label, summary)

@app.route("/metadata/", methods=["PUT"])
def update_metadata():
    pass

@app.route("/chunks/", methods=["POST"])
def create_chunk():
    data = request.json
    text = data.get("text", "")
    source = data.get("source", "")
    parent_id = data.get("parentId", "")

    metadata = {
        "source": source,
        "parent_id": parent_id
    }
    doc_id = str(uuid4())
    lang_doc = Document(page_content=text, id=doc_id, metadata=metadata)
    vectorstore.add_documents(documents=[lang_doc])

    return doc_id
    

@app.route("/add_document/", methods=["POST"])
def embed_text():
    data = request.json
    url = data.get("url", "")
    title = data.get("title", "")
    text = data.get("text", "")

    doc = DocumentPayload(title, url, text)
    lang_doc = Document(page_content=text, id=doc.id, metadata=doc.to_metadata())
    
    vectorstore.add_documents(documents=[lang_doc])

    return doc.to_json()

@app.route("/search/", methods=["GET"])
def search():
    query = request.args.get("q", "")
    results = vectorstore.similarity_search_with_score(query)
    response = []
    for lang_doc, score in results:
        title = lang_doc.metadata['title']
        url = lang_doc.metadata['url']
        text = lang_doc.page_content
        doc = DocumentPayload(title, url, text)
        response.append({
            "score": float(score),
            "doc": doc.to_dict()
        })
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
