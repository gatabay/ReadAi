from operations import parse_article
from flask import Flask, request, abort, jsonify


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/parse", methods=['POST'])
def parse():
    if not request.is_json:
        abort(400)

    arguments = request.json
    
    url = arguments.get("url", None)

    if not url:
        abort(400)
    
    return jsonify(parse_article(url))


if __name__ == "__main__":
    app.run(debug=True)
