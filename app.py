from flask import Flask, render_template, url_for, request, redirect, flash, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = '6c1f69b24eb139bf12725a46b3c311ba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    birthdate = db.Column('birthdate', db.Date, nullable=False)
    age = db.Column('age', db.Integer)
    days_till = db.Column('days_left', db.Integer)
    born_month = db.Column('born_month', db.Integer)

    def __repr__(self):
        return f"User('{self.name}', '{self.birthdate}', '{self.age}', '{self.days_till}')"


@app.route("/", methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        user_name = request.form['name']
        user_birthdate = request.form['birthdate']
        new_bday = datetime.strptime(user_birthdate, "%m-%d-%Y")
        user_age = calculate_age(new_bday)
        days_till = days_till_b(new_bday)
        born_month = new_bday.month
        new_user = User(name=user_name, birthdate=new_bday, age=user_age, days_till=days_till, born_month=born_month)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding a new birthday. Try again!"

    else:
        users = User.query.all()
        now = datetime.now()
        current_month = now.month
        today = now.day
        return render_template("home.html", users=users, current_month=current_month, today=today)


@app.route("/calendar")
def calendar():
    users = User.query.all()
    return render_template("calendar.html", title="Monthly View", users=users)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the contact'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.name = request.form['name']
        birthdate = request.form['birthdate']
        user.birthdate = datetime.strptime(birthdate, "%Y-%m-%d")

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your contact'

    else:
        return render_template('update.html', user=user)


def calculate_age(born):
    """Calculate user's age"""
    today = datetime.now()
    if today.year == born.year:
        return (today.month, today.day) < (born.month, born.day)
    else:
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def days_till_b(born):
    """Calculate how many days left till user's birthday"""
    now = datetime.now()
    delta1 = datetime(now.year, born.month, born.day)
    delta2 = datetime(now.year + 1, born.month, born.day)
    if born.month == now.month and born.day == now.day:
        return 0

    days = ((delta1 if delta1 > now else delta2) - now).days
    return days + 1


# -----------------MICROSERVICE-----------------
@app.route("/wishes", methods=['POST', 'GET'])
def messages():
    keyword = ''
    if request.method == 'POST':
        keyword = request.form['name']

        with open('wish-microservice/relationship.txt', 'w') as f:
            f.write(keyword)

    time.sleep(.5)
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "wishes.json")
    data1 = json.load(open(json_url))
    data = data1['greetings']
    return render_template("wishes.html", title="Birthday Messages", data=data, keyword=keyword)


if __name__ == "__main__":
    app.run(debug=True)
