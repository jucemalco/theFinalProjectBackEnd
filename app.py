import os 
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, Categories, Books, Favorite, Match, Product 

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, "app.db")
Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route("/user", methods = ["POST"])
def create_user():
    user = User()
    user.name = request.json.get("name")
    user.nickname = request.json.get("nickname")
    user.email = request.json.get("email")
    user.password = request.json.get("password")

    if user.name == "":
        return jsonify({
            "msg": "Name can not be empty"
        }), 400 

    if user.email == "":
         return jsonify({
            "msg": "Name can not be empty"
        }), 400 

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 200

@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    users = list(map(lambda user: user.serialize(), all_users))

    return jsonify(users), 200

@app.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
        user = User.query.get(id)
        if user is not None:
            user.nickname = request.json.get("nickname")
            db.session.commit()
            return jsonify(user.serialize()), 200
        else: return jsonify({"msg": "User not found"}), 404

#FALTA EL DELETE PARA ELIMINAR USUARIO


@app.route("/product", methods = ["POST"])
def create_product():
    product = Product()
    title = request.json.get("title")
    autor = request.json.get("autor")
    editorial = request.json.get("editorial")

    product.title = title
    product.autor = autor 
    product.editorial = editorial

    if title == "":
        return jsonify({
            "msg": "Title cannot be empty"
        }), 400
    
    db.session.add(product)
    db.session.commit()

    return jsonify(product.serialize()), 200

@app.route("/products", methods = ["GET"])
def get_products():
    products = Product.query.all()
    products = list(map(lambda product:   product.serialize(),products))

    return jsonify(products), 200

@app.route("/product/<int:id>", methods = ["PUT", "DELETE"])
def update_product(id):
    if request.method == "PUT":
        product = Product.query.get(id)
        if product is not None:
            product.title = request.json.get("title")
            db.session.commit()
            return jsonify(product.serialize()), 200
        else: return jsonify({"msg":"Not found"}), 404
    else:
        product = Product.query.get(id)
        if product is not None:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"msg": "done"})
        else: return jsonify({"msg":"Not found"}), 404


if __name__ == "__main__":
    app.run(host="localhost",port="5000")

