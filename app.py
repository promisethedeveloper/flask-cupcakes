"""Flask app for Cupcakes"""
from types import MethodDescriptorType
from flask import Flask, request, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "4534gdghjk5d#$RGR^HDG"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def index_page():
    # cupcakes = Cupcake.query.all()
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_cupcakes():
    """Get data about all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, 
    rating and image data from the body of the request.
    """
    data = request.json

    cup_cake = Cupcake(flavor=data["flavor"], rating=data["rating"], size=data["size"], image=data["image"] or None)
    db.session.add(cup_cake)
    db.session.commit()
    response_json = jsonify(cupcake=cup_cake.serialize()) 
    return (response_json, 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data.get("flavor", cupcake.flavor)
    cupcake.rating = data.get("rating", cupcake.rating)
    cupcake.size = data.get("size", cupcake.size)
    cupcake.image = data.get("image", cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

    
@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")
    # return jsonify(deleted=todo_id)