from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class HolidayForChildren(db.Model):
    id = db.Column(db.Integer,  nullable=False,  primary_key=True, autoincrement=True)
    price = db.Column(db.Integer, nullable=False, unique=False)
    duration = db.Column(db.Integer, nullable=False, unique=False)
    children_number = db.Column(db.Integer, nullable=False, unique=False)
    age_category = db.Column(db.Integer, nullable=False, unique=False)

    def __init__(self, price, duration, children_number, age_category):
        self.price = price
        self.duration = duration
        self.children_number = children_number
        self.age_category = age_category

    def __del__(self):
        print("Destructor called")


class HolidaySchema(ma.Schema):
    class Meta:
        fields = ('price', 'duration', 'children_number', 'age_category')


holiday_schema = HolidaySchema()
holidays_schema = HolidaySchema(many=True)


@app.route("/user", methods=["POST"])
def add_user():
    price = request.json['price']
    duration = request.json['duration']
    children_number = request.json['children_number']
    age_category = request.json['age_category']
    new_holiday = HolidayForChildren(price, duration, children_number, age_category)

    db.session.add(new_holiday)
    db.session.commit()

    return "SAVED"


@app.route("/user", methods=["GET"])
def get_holiday():
    all_animators = HolidayForChildren.query.all()
    result = holidays_schema.dump(all_animators)
    return jsonify(result.data)


@app.route("/user/<id>", methods=["GET"])
def holiday_detail(id):
    holiday = HolidayForChildren.query.get(id)
    return holiday_schema.jsonify(holiday)


@app.route("/user/<id>", methods=["PUT"])
def holiday_update(id):
    holiday = HolidayForChildren.query.get(id)
    price = request.json['price']
    duration = request.json['duration']
    children_number = request.json['children_number']
    age_category = request.json['age_category']

    holiday.price = price
    holiday.duration = duration
    holiday.children_number = children_number
    holiday.age_category = age_category

    db.session.commit()
    return "UPDATED"


@app.route("/user/<id>", methods=["DELETE"])
def holiday_delete(id):
    holiday = HolidayForChildren.query.get(id)
    db.session.delete(holiday)
    db.session.commit()

    return "DELETED"


if __name__ == '__main__':
    app.run()



