from operations import parse_article
from flask import Flask, request, abort, jsonify, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/read", methods=['POST'])
def read():
    arguments = request.form
    
    url = arguments.get("url", None)

    if not url:
        abort(400)

    words, markups = parse_article(url)

    return render_template("read.html", words=words, markups=markups)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
