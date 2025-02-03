from flask import Flask, request, jsonify

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="nlpaueb/legal-bert-base-uncased")

app = Flask(__name__)

@app.route("/embed/", methods=["POST"])
def embed_text():
    data = request.json
    text = data.get("text", "")
    embedding = embeddings.embed_query(text)
    return jsonify({"embedding": embedding})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
