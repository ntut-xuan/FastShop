from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Hello World"

app.debug = True
app.run(host="0.0.0.0", port="8080")