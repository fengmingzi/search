from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
