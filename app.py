from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(125), unique=True)
    year = db.Column(db.Integer)
    no_of_tracks = db.Column(db.Integer)

    def __init__(self, name, year, no_of_tracks):
        self.name = name
        self.year = year
        self.no_of_tracks = no_of_tracks

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer)
    name = db.Column(db.String(100), unique=True)
    length = db.Column(db.Float)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

    def __init__(self, name, album_id):
        self.name = name
        self.album_id = album_id

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'year', 'no_of_tracks')

class SongsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'no', 'name', 'length', 'album_id')

album_schema = AlbumSchema()
song_schema = SongsSchema()
albums_schema = AlbumSchema(many=True)
songs_schema = SongsSchema(many=True)

@app.route('/album', methods=['POST'])
def add_album():
    name = request.json['name']
    year = request.json['year']
    no_of_tracks = request.json['no_of_tracks']

    new_album = Albums(name, year, no_of_tracks)

    db.session.add(new_album)
    db.session.commit()

    return album_schema.jsonify(new_album)

@app.route('/album/', methods=['GET'])
def get_albums():
    all_albums = Albums.query.all()
    result = albums_schema.dump(all_albums)
    return jsonify(result)

@app.route('/album/<id>', methods=['GET'])
def show_album(id):
    album = Albums.query.get(id)
    return album_schema.jsonify(album)

if __name__ == '__main__':
    app.run(debug=True)
