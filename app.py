from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hi from Flask, give me some food<h1>"

if __name__ == '__main__':
    app.debug = True
    app.run()