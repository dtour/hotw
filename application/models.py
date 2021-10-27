import datetime
from application import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    week = db.Column(db.Integer, default=datetime.datetime.utcnow().isocalendar().week)
    submission_text = db.Column(db.Text, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'group_id','week'),)

membership = db.Table('membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    
    membership = db.relationship('Group', secondary=membership, lazy='subquery',
        backref=db.backref('members', lazy=True))

    def get_reset_token(self, expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}')"

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Group('{self.name}')"
    
    def get_join_group_token(self, expires_sec=604800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'group_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_join_group_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            group_id = s.loads(token)['group_id']
        except:
            return None
        return Group.query.get(group_id)