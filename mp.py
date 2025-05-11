from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1:3306/mp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    magazine_name = db.Column(db.String(100))
    copies = db.Column(db.Integer)
    total_amount = db.Column(db.Integer)       
    payment_method = db.Column(db.String(50))
    payment_detail1 = db.Column(db.String(100))           
    payment_detail2 = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        suggestion = Suggestion(name=name, message=message)
        db.session.add(suggestion)
        db.session.commit()
    return render_template("home.html")

@app.route("/membership", methods=['GET', 'POST'])
def membership():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form.get('email')
        address = request.form.get('address')
        member = Membership(name=name, mobile=mobile, email=email, address=address)
        db.session.add(member)
        db.session.commit()
    return render_template("membership.html")


@app.route("/order", methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        address = request.form.get('address')
        magazine_name = request.form.get('magazine_name')
        copies = int(request.form.get('copies', 0))
        total_amount = int(request.form.get('total_amount') or 0)
        payment_method = request.form.get('payment_method')
        payment_detail1 = request.form.get('payment_detail1')
        payment_detail2 = request.form.get('payment_detail2')
        

        order = Order(
            name=name,
            contact=contact,
            address=address,
            magazine_name=magazine_name,
            copies=copies,
            
            total_amount=total_amount,
            payment_method=payment_method,
            payment_detail1=payment_detail1,
            payment_detail2=payment_detail2,
           
        )
        db.session.add(order)
        db.session.commit()
        return render_template("order.html", success=True, name=name,copies=copies, amount=total_amount) # alert popup for successful Transaction
    return render_template("order.html", success=False) # if false Transaction





if __name__ == "__main__":
    with app.app_context():  
        # db.drop_all() # used for altering the table to add payment detail 1 and 2
        db.create_all()
    app.run(debug=True)
