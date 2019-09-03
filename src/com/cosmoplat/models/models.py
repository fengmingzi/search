
from app import db

'''定义模型，建立关系'''
# class Role(db.Model):#所有模型的基类叫 db.Model，它存储在创建的SQLAlchemy实例上。
#     #定义表名
#     __tablename__ = 'roles'
#
#     #定义对象
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     user = db.relationship('User', backref='role')
#
#     #__repr__()方法显示一个可读字符串，虽然不是完全必要，不过用于调试、测试是很不错的。
#     def __repr__(self):
#         return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.name)