from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    choices_c = [("✘"),("☕️"),("☕️☕️"),("☕️☕️☕️"),("☕️☕️☕️☕️"),("☕️☕️☕️☕️☕️")]
    choices_w = [("✘"),("💪"),("💪💪"),("💪💪💪"),("💪💪💪💪"),("💪💪💪💪💪")]
    choices_p = [("✘"),("🔌"),("🔌🔌"),("🔌🔌🔌"),("🔌🔌🔌🔌"),("🔌🔌🔌🔌🔌")]
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location',validators=[DataRequired(),url(message="Please enter a valid url.")])
    open = StringField('Open Time')
    close = StringField('Close Time')
    coffee = SelectField('Coffee',choices=choices_c)
    wifi = SelectField('Wi-Fi Strength',choices=choices_w)
    power = SelectField("Power",choices=choices_p)
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["POST","GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_form = f"{form.cafe.data},{form.location.data},{form.open.data},{form.close.data}, {form.wifi.data},{form.coffee.data},{form.power.data}"
        with open('cafe-data.csv','a',encoding='UTF-8') as file:
            file.write(f"\n{new_form}")
    return render_template('add.html', form=form)
@app.route('/cafes')
def cafes():
    form = CafeForm()
    with open('cafe-data.csv', newline='',encoding='UTF-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        more_ = False
        for row in csv_data:
            list_of_rows.append(row)
            print(list_of_rows)
            if len(list_of_rows) >= 5:
                more_=True
    return render_template('cafes.html', cafes=list_of_rows,more=more_)


if __name__ == '__main__':
    app.run(debug=True)
