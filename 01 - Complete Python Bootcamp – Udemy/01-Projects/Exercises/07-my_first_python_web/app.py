from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/otra")
def otra_pagina():
    return render_template("otra.html")

if __name__ == "__main__":
    app.run(debug=True)