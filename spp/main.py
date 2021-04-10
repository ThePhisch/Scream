import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Scream Social: Under Construction</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0")

def test():
    print("this is an import test")
    print(os.getenv('DB_USER'))

