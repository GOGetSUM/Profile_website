import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, email_validator

#~~~~~~~~~~~~~~~~~~~~~create flask app~~~~~~~~~~~~~~~~~

app = Flask(__name__)
#--------------------create new data base for messages---------------------------------
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "sqlite:///visitors.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
#---------------------create new table for messages--------------------------------------------------
class Message(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstName = db.Column(db.String(50), unique=False, nullable=False)
    lastName = db.Column(db.String(50), unique=False, nullable=True)
    email = db.Column(db.String(100), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False,nullable=False)
    message = db.Column(db.String(500), unique=False,nullable=False)
db.create_all()

#---------------------create record----------------------------------------------------------------
# visitor_message = Message(
#     id = 1,
#     firstName = 'Nicolas',
#     lastName = 'Corona',
#     email = 'nick.d.corona@gmail.com',
#     phone = '5625057286',
#     message ='hjkhdskjhfskadhkjshadkhjsfadlkfsdhksjhsdklfhsdkfj'
# )
#
# db.session.add(visitor_message)
# db.session.commit()
#-----------------------create form for visitor message---------------------------------------------------------------
class addMessageForm(FlaskForm):
    firstName = StringField("First Name", validators=[DataRequired()])
    lastName = StringField("Last Name",)
    email = StringField("Email")
    phone = StringField("Phone",)
    message =StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")


# Home _ Index ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/',methods=["GET", "POST"])
def home():
    form = addMessageForm()
    if form.validate_on_submit():
        id_prev = Message.query.order_by(Message.id).all()
        id_new = len(id_prev) + 1
        New_Message = Message(
            id = id_new,
            firstName = form.firstName.data,
            lastName = form.lastName.data,
            email = form.email.data,
            phone = form.phone.data,
            message = form.message.data)
        db.session.add(New_Message)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', form=form)


# @app.route("/add_msg", methods=["GET", "POST"])
# def receive_datat():
#     id_prev = Message.query.order_by(Message.id).all()
#     id_new = len(id_prev) + 1
#     New_Message = Message(
#         id = id_new,
#         firstName = request.form['firstName'],
#         lastName = request.form['lasttName'],
#         email = request.form['email'],
#         phone = request.form['phone'],
#         message = request.form['message'])
#     db.session.add(New_Message)
#     db.session.commit()
#     return redirect(url_for('home'))



#--------run app------------------------
if __name__=='__main__':
    app.run(debug=True)
