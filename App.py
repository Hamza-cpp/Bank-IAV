from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/list")
def lit_test():
    return ["hi", "how are you"]


@app.route("/json")
def lit_test():
    return {
        "name": "youssef",
        "prenom": "ellouh",
        "password": "ydnduèjej22",
        "email": "test@gmail.com",
    }
