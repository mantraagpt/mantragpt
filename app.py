from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SCOPUS_API_KEY = "0f08decc13e583025faccadb7cfe29e6"
SCOPUS_ENDPOINT = "https://api.elsevier.com/content/search/scopus"

@app.route("/scopus/search", methods=["GET"])
def search_scopus():
    query = request.args.get("query")
    count = request.args.get("count", "5")
    date = request.args.get("date")

    if not query:
        return jsonify({"error": "Parameter 'query' wajib diisi"}), 400

    params = {
        "query": query,
        "count": count,
    }
    if date:
        params["date"] = date

    headers = {
        "X-ELS-APIKey": SCOPUS_API_KEY
    }

    try:
        response = requests.get(SCOPUS_ENDPOINT, params=params, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": str(e), "detail": response.text}), response.status_code

@app.route("/", methods=["GET"])
def index():
    return "✅ Scopus Search API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
