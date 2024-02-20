from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/list")
def lit_test():
    return ["hi", 'how are you']
