from flask_login import UserMixin
import flask_whooshalchemy as wa
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager, appname

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):

        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# genres = db.Table('genres',
#                   db.Column('anime_id', db.Integer, db.ForeignKey('anime.id')),
#                   db.Column('genres_id'), db.Integer, db.ForeignKey('genres.id'))

class Anime(db.Model):
    __tablename__ = 'animes'
    __searchable__ = ['title', 'genres', 'studios']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    sypnosis = db.Column(db.String(1000))
    genres = db.Column(db.String(100))
    imagesrc = db.Column(db.String(100))
    studios = db.Column(db.String(100))
    # genres = db.relationship('Genres', backref='anime', lazy='dynamic')

    def __repr__(self):
        return '<Anime: {}>'.format(self.name)

wa.whoosh_index(appname, Anime)

class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(100), unique=True)
    # anime_id = db.Column(db.Integer, db.ForeignKey('animes.id'))

