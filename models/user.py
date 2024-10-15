from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), index=True)
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # def __init__(self, username, email, password, role="user"):
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.role = role

    def __repr__(self):
        return f"<User email={self.email}, username={self.username}, password={self.password}, role={self.role}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
