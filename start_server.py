# coding=utf-8
from flask import Flask, render_template, Response, request, send_from_directory
import os

app = Flask(__name__, static_folder="./dashboard/assets")
@app.route('/')  # 主页
def index():
    if os.path.isfile("./dashboard/index.html") == True:
        with open("./dashboard/index.html", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/html') 
    else:
     return "404 Not found", 404
@app.route('/index.html')  # 主页
def index1():
    if os.path.isfile("./dashboard/index.html") == True:
        with open("./dashboard/index.html", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/html') 
    else:
     return "404 Not found", 404

@app.route('/dashboard/data.json')
def get_data(): 
    print("Get data")
    if os.path.isfile("./dashboard/data.json") == True:
        with open("./dashboard/data.json", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/plain') 
    else:
     return "404 Not found", 404
@app.route('/dashboard/index_data.json')
def get_data1(): 
    print("Get data")
    if os.path.isfile("./dashboard/index_data.json") == True:
        with open("./dashboard/index_data.json", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/plain') 
    else:
     return "404 Not found", 404

@app.route('/dashboard/update_date.json')
def get_data2(): 
    print("Get data")
    if os.path.isfile("./dashboard/update_date.json") == True:
        with open("./dashboard/update_date.json", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/plain') 
    else:
     return "404 Not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)