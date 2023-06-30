from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=True)
    status = db.Column(db.String(10), default='inactive')

    def __repr__(self):
        return '<Project {}>'.format(self.description)
