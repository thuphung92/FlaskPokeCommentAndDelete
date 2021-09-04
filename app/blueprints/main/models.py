from app import db
from datetime import datetime as dt

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    ability = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    sprite_url = db.Column(db.String(200))
    
    comments = db.relationship('Comment', backref='poke', lazy='dynamic')

    def __repr__(self):
        return f'<Pokemon ID: {self.id} | Name: {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    pokemon_id = db.Column(db.Integer(), db.ForeignKey("pokemon.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f'<Comment ID: {self.id} | Body: {self.body.truncate(20)}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()