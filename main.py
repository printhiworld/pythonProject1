from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from raw_data import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


with app.app_context():
    db.create_all()

    for user in users:
        db.session.add(User(**user))
        db.session.commit()

    for _ in offers:
        db.session.add(Offer(**_))
        db.session.commit()

    for _ in orders:
        db.session.add(Order(**_))
        db.session.commit()



@app.route("/user/<int:uid>")
def user(uid):
    if request.method == 'GET':
        user = User.query.get(uid).to_dict()
        return jsonify(user)
    if request.method == 'DELETE':
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return '', 202
    if request.method == 'PUT':
        user_data = request.json
        user = User.query.get(uid)

        if user.data.get('first_name'):
            user.first_name = user_data['first_name']
        if user.data.get('last_name'):
            user.last_name = user_data['last_name']
        if user.data.get('age'):
            user.age = user_data['age']
        if user.data.get('email'):
            user.email = user_data['email']
        if user.data.get('role'):
            user.role = user_data['role']
        if user.data.get('phone'):
            user.phone = user_data['phone']


        db.session.add(user)
        db.session.commit()
        return '', 202


@app.route("/user")
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    if request.method == 'POST':
        user_data = request.json
        db.session.add(User(**user_data))
        db.session.commit()
        return '', 201



@app.route("/order/<int:uid>")
def order(uid):
    if request.method == 'GET':
        order = Order.query.get(uid).to_dict()
        return jsonify(order)
    if request.method == 'DELETE':
        order = Order.query.get(uid)
        db.session.delete(order)
        db.session.commit()
        return '', 202
    if request.method == 'PUT':
        order_data = request.json
        order = Order.query.get(uid)


        if order.data.get('name'):
            order.first_name = order_data['name']
        if order.data.get('description'):
            order.last_name = order_data['description']
        if order.data.get('start_date'):
            order.age = order_data['start_date']
        if order.data.get('end_date'):
            order.email = order_data['end_date']
        if order.data.get('price'):
            order.role = order_data['price']
        if order.data.get('customer_id'):
            order.phone = order_data['customer_id']
        if order.data.get('executor_id'):
            order.phone = order_data['executor_id']



        db.session.add(order)
        db.session.commit()
        return '', 202


@app.route("/orders")
def orders():
    if request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders])
    if request.method == 'POST':
        order_data = request.json
        db.session.add(User(**order_data))
        db.session.commit()
        return '', 201


@app.route("/offer/<int:uid>")
def offer(uid):
    if request.method == 'GET':
        offer = Offer.query.get(uid).to_dict()
        return jsonify(offer)
    if request.method == 'DELETE':
        offer = Offer.query.get(uid)
        db.session.delete(offer)
        db.session.commit()
        return '', 202
    if request.method == 'PUT':
        offer_data = request.json
        offer = Order.query.get(uid)


        if offer.data.get('order_id'):
            offer.phone = offer_data['order_id']
        if offer.data.get('executor_id'):
            offer.phone = offer_data['executor_id']



        db.session.add(offer)
        db.session.commit()
        return '', 202


@app.route("/offers")
def offers():
    if request.method == 'GET':
        offers = Order.query.all()
        return jsonify([offer.to_dict() for offer in offers])
    if request.method == 'POST':
        offer_data = request.json
        db.session.add(User(**offer_data))
        db.session.commit()
        return '', 201




if __name__=='__main__':
    app.run()