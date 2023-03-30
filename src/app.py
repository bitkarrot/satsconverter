from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", title="Sats Converter")
#    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'