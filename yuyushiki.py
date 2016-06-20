# -*- coding: utf-8 -*-
import atexit
from functools import reduce
from pathlib import Path

from flask import Flask, render_template, send_from_directory, request, send_file
from pymongo import Connection

from os import path
import json

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

con = Connection('localhost', 27017)
collection = con.yuyushiki.comics
atexit.register(con.close)

root = Path('data')
pages = reduce(lambda a, b:a+b, [[p for p in path.iterdir()] for path in root.iterdir()])
pages.sort()

# load config.json
json_path = path.join(path.abspath(path.dirname(__file__)), 'config.json')
with open(json_path) as data_file:
    config = json.load(data_file)


def get_latest():
    latest = list(collection.find({}).sort('_id',-1).limit(1))
    if latest == []:
        return pages[0]
    else:
        i = pages.index(Path(latest[0]['path']))
        return pages[i+1] 

def get_tag_latest():
    latest = list(collection.find({'characters':[]}).limit(1))
    if latest == [] and collection.count() > 0:
        return get_latest()
    if latest == []:
        return pages[0]
    else:
        i = pages.index(Path(latest[0]['path']))
        return pages[i] 

def find_one(path):
    return collection.find_one({'path':path})

def upsert(path, script='', characters=[], reedit=False, useless=False):
    d = {'path':path, 'script':script, 'characters':characters,
            'reedit':reedit, 'useless':useless}
    collection.update({'path':path}, d, upsert=True) 

# TODO: complete画面, pagesの最後
@app.route('/', methods=['GET', 'POST'])
def index():
    prev = False
    if request.method == 'POST':
        data = request.form
        if data.get('action') == 'prev':
            path = data.get('path')
            prev = True
        else:
            path = data.get('path')
            characters = list(filter(bool, data.getlist('characters')))
            if characters == []:
                characters.append('none')
            data = find_one(path)
            if data:
                data['characters'] = characters
                collection.update({'path':path}, data, upsert=True) 
            else:
                upsert(path, characters=characters)

        i = pages.index(Path(path))
        if prev:
            if i - 1 < 0:
                p = pages[i]
            else:
                p = pages[i-1]
        else:
            try:
                p = pages[i+1]
            except IndexError:
                return render_template('finish.html')
    elif request.method == 'GET':
        p = get_tag_latest()

    data = find_one(p.as_posix())
    p = Path(data['path']) if data else p
    characters = {c:True for c in data['characters']} if data else []
    progress = round(collection.find({'characters':{'$ne':[]}}).count() * 100 / len(pages), 2)
    return render_template('index.html', path=p, progress=progress, characters=characters)

@app.route('/data/<path:filename>')
def data(filename):
    return send_from_directory(root.as_posix(), filename)

@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory('img', filename)

@app.route('/js/main.js')
def mainjs():
    return send_file('templates/main.js')

@app.route('/js/lib/<path:filename>')
def js(filename):
    return send_from_directory('templates/lib', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
