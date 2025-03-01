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

@app.route("/metadata/", methods=["GET"])
def get_metadata():
    conn = create_default_connection()
    label = request.args.get('label')
    try:
        row_id, parent_id, datatype, label, summary = find_one_text_embedding_metadata(conn, label)
        return jsonify({"id": row_id, "parentId": parent_id, "datatype": datatype, "label": label, "summary": summary})
    except Exception as e:
        return jsonify({})

# parent_id, datatype, label, summary) VALUES (%s, %s, %s, %s)",
@app.route("/metadata/", methods=["POST"])
def create_metadata():
    data = request.json
    parent_id = data.get("parentId", "")
    datatype = data.get("datatype", "")
    label = data.get("label", "")[:255]
    summary = ''

    conn = create_default_connection()
    create_text_embedding_metadata(conn, parent_id, datatype, label, summary)
    row_id, parent_id, datatype, label, summary = find_one_text_embedding_metadata(conn, label)
    return jsonify({"id": row_id, "parentId": parent_id, "datatype": datatype, "label": label, "summary": summary})

# This only updates `summary` right now`
@app.route("/metadata/", methods=["PUT"])
def update_metadata():
    section_id = request.args.get('id')
    data = request.json
    summary = data.get("summary", "")

    try:
        conn = create_default_connection()
        add_summary(conn, section_id, summary)
        return jsonify({"error": False})
    except Exception as e:
        print(e)
        return jsonify({"error": True})

@app.route("/sections/", methods=["GET"])
def http_get_section_by_id():
    conn = create_default_connection()
    section_id = request.args.get('id')
    try:
        # retrieve all the metadata for the section in the SQL database
        row_id, parent_id, datatype, label, summary = find_one_text_embedding_metadata_by_id(conn, section_id)

        # retrieve all the chunks for the section from the vector store
        chunks = vectorstore.get(where={"parent_id": int(section_id)})
        return jsonify({
            "section": {
                "id": row_id,
                "parentId": parent_id,
                "datatype": datatype,
                "label": label,
                "summary": summary
            },
            "chunks": chunks['documents']
        })
    except Exception as e:
        return jsonify({ "section": {}, "chunks": []})

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

    return jsonify({"id": doc_id})
    

@app.route("/add_document/", methods=["POST"])
def embed_text():
    data = request.json
    url = data.get("url", "")
    text = data.get("text", "")
    chunk_index = data.get("chunk_index", -1)
    breakpoint()

    doc = DocumentPayload(url, text, chunk_index)
    lang_doc = Document(page_content=text, id=doc.id, metadata=doc.to_metadata())
    
    vectorstore.add_documents(documents=[lang_doc])

    return doc.to_json()

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

@app.route("/documents/", methods=["GET"])
def documents_index():
    docs = vectorstore.get()
    response = []
    breakpoint()
    for text  in docs['documents']:
        title = lang_doc.metadata['title']
        url = lang_doc.metadata['url'] 
        text = lang_doc.page_content
        doc = DocumentPayload(title, url, text)
        response.append(doc.to_dict())
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
