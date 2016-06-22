# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, send_file, redirect, url_for

from face import Face

from os import path
import json

app = Flask(__name__)
app.config.update(
    DEBUG=True,
)

# TODO: rectangle, pics

# load config.json
json_path = path.join(path.abspath(path.dirname(__file__)), 'config.json')
with open(json_path) as data_file:
    config = json.load(data_file)

@app.route('/')
def index():
    next_face = Face.select().where(Face.character == None).first()
    if next_face:
        return redirect(url_for("index_id", id = next_face.id))
    else:
        return redirect(url_for("finish"))

@app.route('/<id>', methods=['GET', 'POST'])
def index_id(id):
    if request.method == 'POST':
        data = request.form
        c = data.get('character')
        if c and c != config["skip_tag"]:
            print(c)
            query = Face.update(character = c).where(Face.id == id)
            query.execute()
        next_id = int(id) + 1
        return redirect(url_for("index_id", id = next_id))

    # get
    else:
        next_face = Face.select().where(Face.id == id).first()
        if not next_face:
            return redirect(url_for("finish"))

        progress = round(Face.select().where(Face.character != None).count() * 100 / Face.select().count(), 2)
        return render_template('index.html', face=next_face, progress=progress, config=config)

@app.route('/finish')
def finish():
    return render_template('finish.html', config=config)

@app.route('/faces/<path:filename>')
def faces(filename):
    return send_from_directory('faces', filename)

@app.route('/shots/<path:filename>')
def shots(filename):
    return send_from_directory('shots', filename)

@app.route('/img/<path:filename>')
def img(filename):
    return send_from_directory('img', filename)

@app.route('/js/lib/<path:filename>')
def js(filename):
    return send_from_directory('templates/lib', filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('img', "favicon.ico")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
