# coding=utf-8
from flask import Flask, render_template, Response, request, send_from_directory
import os

app = Flask(__name__, static_folder="./templates/assets")
@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')
@app.route('/index.html')  # 主页
def index1():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('index.html')


@app.route('/data.json')
def get_data(): 
    print("Get data")
    if os.path.isfile("./templates/data.json") == True:
        with open("./templates/data.json", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/plain') 
    else:
     return "404 Not found", 404
@app.route('/index_data.json')
def get_data1(): 
    print("Get data")
    if os.path.isfile("./templates/index_data.json") == True:
        with open("./templates/index_data.json", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/plain') 
    else:
     return "404 Not found", 404

@app.route('/update_date.json')
def get_data2(): 
    print("Get data")
    if os.path.isfile("./templates/update_date.json") == True:
        with open("./templates/update_date.json", "r", encoding = 'utf-8') as f:
           return Response(f.read(),
                    mimetype='text/plain') 
    else:
     return "404 Not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)