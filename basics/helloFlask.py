import json

from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm, MultiCheckboxField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'cb8ad7e4ed31f5f27ca78e508b38c523'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

posts = [
    {
        'Database': 'Proton_therapy',
        'column': 'ID',
        'content': 'alpha numeric character',
        'id': 1
    },
    {
        'Database': 'Proton_therapy',
        'column': 'age',
        'content': 'numeric character',
        'id': 2,
        'predicted': ['umar', 'age', 'vay']
    }
]


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form.getlist('mycheckbox'))
        selected_id = request.form.getlist('mycheckbox')
        selected_column = []

        for p in posts:
            for s in selected_id:
                if int(p["id"]) == int(s):
                    selected_column.append({
                        'Database': p["Database"],
                        'column': p["column"],
                        'content': p["content"],
                        'id': p["id"],
                        'predicted': p["predicted"]
                    })
                    return render_template('predicted.html', posts=selected_column)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/multi", methods=['GET', 'POST'])
def multi():
    if request.method == 'POST':
        print(request.form.getlist('mycheckbox'))
        return 'Done'
    return render_template('multiselect.html')


if __name__ == "__main__":
    app.run(debug=True)
