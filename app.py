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
    name = name = db.Column(db.String(100), unique=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

    def __init__(self, name, album_id):
        self.name = name
        self.album_id = album_id

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'year', 'no_of_tracks')

class SongsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'album_id')

album_schema = AlbumSchema()
song_schema = SongsSchema()
albums_schema = AlbumSchema(many=True)
songs_schema = SongsSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
