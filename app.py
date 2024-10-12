from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    logout_user,
    login_required,
)
from users import router_users

app = Flask(__name__)
app.register_blueprint(router_users, url_prefix="/api")

app.config["SECRET_KEY"] = "s3cr3t"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/users/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # user = User.query.filter_by(username=username).all() # return list of user
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return jsonify({"message": "Authenticated successfully"}), 200
            else:
                return jsonify({"message": "Wrong username or password"}), 401
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "username and password are required"}), 400


@app.route("/users/logout", methods=["GET"])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "User logged out successfully"}), 401

    return jsonify({"message": "User not logged in"}), 401


@app.route("/users/add", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if username and email and password:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 201

    return jsonify({"message": "username, email and password are required"}), 400


@app.route("/users/", methods=["GET"])
@login_required
def get_users(): ...


@app.route("/users/one/<int:id_user>", methods=["GET"])
@login_required
def get_user(id_user):
    user = User.query.get(id_user)
    print(user)

    if user:
        return jsonify(user.to_dict()), 200

    return jsonify({"message": "User not found"}), 404


@app.route("/users/upd/<int:id_user>", methods=["PUT"])
@login_required
def update_user(id_user):
    user = User.query.get(id_user)
    if user:
        data = request.json
        user.username = data.get("username")
        user.email = data.get("email")
        user.password = data.get("password")
        db.session.commit()
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/del/<int:id_user>", methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello World!"})


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
