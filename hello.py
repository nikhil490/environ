from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/data")
def data():
    return render_template('home.html')

@app.route("/save")
def save():
    print('nikhil')
    response_API = requests.get('https://environment.data.gov.uk/flood-monitoring/data/readings?latest')
    with open('text.txt','a') as f :
        f.write(response_API.text) 

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    response_API = requests.get('https://environment.data.gov.uk/flood-monitoring/data/readings?latest')
    with open('text.txt','a') as f :
        f.write(response_API.text)
    return 'nothing'