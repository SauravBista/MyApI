from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()

@app.route("/random")
def random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
        "id": random_cafe.id,
        "name": random_cafe.name,
        "map_url": random_cafe.map_url,
        "locaiton": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price



    })


@app.route("/all")
def all_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafe_list = []
    for cafe in all_cafes:
        cafe_list.append({
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "locaiton": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price
        })
    return jsonify(cafes=cafe_list)

# routing looks like http://127.0.0.1:5000/select?location=Peckham
@app.route("/select")
def find_cafe():
    location = request.args.get("location")

    if location:
        result = db.session.execute(db.select(Cafe).filter_by(location=location))
        cafes = result.scalars().all()

        if cafes:
            cafe_list =[]
            for cafe in cafes:
                cafe_list.append({
                "id": cafe.id,
                "name": cafe.name,
                "map_url": cafe.map_url,
                "locaiton": cafe.location,
                "seats": cafe.seats,
                "has_toilet": cafe.has_toilet,
                "has_wifi": cafe.has_wifi,
                "has_sockets": cafe.has_sockets,
                "can_take_calls": cafe.can_take_calls,
                "coffee_price": cafe.coffee_price
                })
            return jsonify(cafes=cafe_list)
        else:
            return jsonify({
                "error": "No Cafes in this locaiton"
            }), 404
    else:
        return jsonify({
            "error": "Location paramater needed "
        }), 400


@app.route("/add", methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

@app.route("/update_price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id):
    cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalars().first()
    new_price = request.args.get("new_price")
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify({
            "success": "Successfully updated the coffee price" 
        })
    else:
        return jsonify({
            "error": {
                "Not found": "Sorry a cafe with that id doesnot exist"
            }
        }), 404


@app.route("/report_closed/<int:cafe_id>", methods=['DELETE'])
def delete(cafe_id):
    private_key = "this-is-top-secret"
    cafe = db.session.execute(db.select(Cafe).filter_by(id=cafe_id)).scalars().first()
    api_key = request.args.get("api_key")
    if cafe:
        if api_key == private_key:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify({
                "Success": "The cafe is deleted"
            })
        else:
            return jsonify({
                "error": "api key doesnt match"
            })
    else:
        return jsonify({
            "error": "No cafe with that id"
        })

@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
