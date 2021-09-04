from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from app.blueprints.main.models import Pokemon, Comment


catched = db.Table('catched',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('poke_id', db.Integer, db.ForeignKey('pokemon.id')),
        db.Column('catched_on',db.DateTime, default=dt.utcnow)
)

# Each class here represents a table in the database
class User(UserMixin, db.Model): # multiple inheritence (order is important)
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email =  db.Column(db.String(200), unique=True, index=True) # add index = True helps sql works faster
    password = db.Column(db.String(200))
    icon = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    poke_catched = db.relationship('Pokemon', secondary = catched, backref = db.backref('owners', lazy = 'dynamic'))

    def __repr__(self): # unique identifier of an object
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']
        self.save()

    def get_icon_url(self):
        return f"https://avatars.dicebear.com/api/bottts/{self.icon}.svg"

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password,login_password)

    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #saves the changes into the db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))