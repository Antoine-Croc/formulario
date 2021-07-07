from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "this doesn't work!"

app.run(debug=True)