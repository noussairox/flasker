from flask import Flask, redirect, url_for, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# => Add database
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIOS'] = True
# => secret key
app.config['SECRET_KEY'] = 'mysecretkey'
# => Initialiser database
db = SQLAlchemy(app)


class Names(db.Model):  # => Create a model
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Names %r>' % self.names


class Users(db.Model):  # => Create a model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # => Create a String (fonction qui retourne un string)

    def __repr__(self):
        return '<Name %r>' % self.name


@app.errorhandler(404)  # invalid url
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)  # Internal Server Error
def page_not_found(e):
    return render_template("500.html"), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


class userform(FlaskForm):  # create a form class
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class namerform(FlaskForm):  # create a form class
    names = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/name", methods=["GET", "POST"])  # => Create name Page
def name():
    names = None
    form = namerform()
    if form.validate_on_submit():
        username = Names.query.filter_by(names=form.names.data).first()
        if username is None:
            username = Names(names=form.names.data)
            db.session.add(username)
            db.session.commit()
        names = form.names.data
        form.names.data = ''
        flash("username add successfuly")
    our_names = Names.query.order_by(Names.date_added)
    return render_template("name.html", form=form, names=names, our_names=our_names)


@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None
    form = userform()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("user add successfuly")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


db.create_all()
db.session.commit()


if __name__ == '__main__':
    app.run(port=5212, debug=True)
