from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, TextAreaField, TimeField
from wtforms.widgets import Input
import datetime

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///reservation.db'
app.config['SECRET_KEY'] = 'qwertypad'
db= SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    num_of_people = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    note = db.Column(db.String(200),nullable=True)

    def __repr__(self):
        return f'<Reservation {self.name}>'

with app.app_context():
    db.create_all()

class TimeField(StringField):
    widget = Input(input_type='time')

class ReservationForm(FlaskForm):
    name = StringField('Name')
    phone_number = StringField('Phone Number')
    num_of_people = SelectField('Number of People', choices=[('1', '1 Person'), ('2', '2 Person'), ('3', '3 Person'), ('4', '4 Person'), ('5', '5 Person'), ('6', '6 Person'), ('7', '7 Person')])
    date = DateField('Date')
    time = TimeField('Time')
    note = TextAreaField('Note')
    submit = SubmitField('Book A Table')


@app.route('/', methods=['GET', 'POST'])
def restaurant():
    form = ReservationForm()
    if form.validate_on_submit():
        time_parts = form.time.data.split(':')
        reservation = Reservation(
            name=form.name.data,
            phone_number=form.phone_number.data,
            num_of_people=int(form.num_of_people.data),
            date=form.date.data,
            time=datetime.time(int(time_parts[0]), int(time_parts[1])),
            note=form.note.data
        )
        db.session.add(reservation)
        db.session.commit()
        return redirect(url_for('restaurant'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)