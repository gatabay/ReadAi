from jpype import startJVM, getDefaultJVMPath, shutdownJVM


from operations import parse_article
from flask import Flask, request, abort, render_template


startJVM(
    getDefaultJVMPath(),
    '-ea',
    f'-Djava.class.path=zemberek-full.jar',
    convertStrings=False
)


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

    words, markups, summary = parse_article(url)

    for key, val in markups.items():
        print(f'NUM {key}: {len(val)}')

    print(f'SUMMARY:\n{summary}')

    return render_template("read.html", words=words, markups=markups, summary=summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    shutdownJVM()
