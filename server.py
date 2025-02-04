from flask import Flask, request, jsonify

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

app = Flask(__name__)

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
