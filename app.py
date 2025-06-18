from flask import Flask, request, jsonify
import pandas as pd
import difflib

app = Flask(__name__)
data = pd.read_csv("data.csv")

def find_best_match(question, data):
    titles = data["title"].tolist()
    matches = difflib.get_close_matches(question, titles, n=2, cutoff=0.3)
    results = []
    for match in matches:
        row = data[data["title"] == match].iloc[0]
        results.append({
            "url": row["url"],
            "text": row["title"]
        })
    return results

@app.route("/api/", methods=["POST"])
def answer_question():
    req = request.get_json()
    question = req.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    matched_links = find_best_match(question, data)
    answer = "Here are the most relevant discussions we found." if matched_links else "Sorry, no relevant discussion found."

    return jsonify({
        "answer": answer,
        "links": matched_links
    })

if __name__ == "__main__":
    app.run(debug=True)

