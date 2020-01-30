from flask import render_template, url_for, flash, redirect, jsonify, request
from recommender.forms import RegistrationForm, LoginForm, MultiCheckboxField
from recommender import app
from recommender.json_traverse_trails import get_column_names

posts = get_column_names()
#[{"id": 0, "column": "Outcome"}, {"id": 1, "column": "PCI"}, {"id": 2, "column": "Geboortemaand"}, {"id": 3, "column": "Geslacht"}, {"id": 4, "column": "Invoerdatum"}, {"id": 5, "column": "VraagType"}, {"id": 6, "column": "Vraagstelling"}, {"id": 7, "column": "Antwoord"}, {"id": 8, "column": "Tumour_Treatment"}, {"id": 9, "column": "PCI"}, {"id": 10, "column": "Geboortemaand"}, {"id": 11, "column": "Geslacht"}, {"id": 12, "column": "Overleden"}, {"id": 13, "column": "Datum overlijden"}, {"id": 14, "column": "Laatste datum check in leven"}, {"id": 15, "column": "Diagnose"}, {"id": 16, "column": "Datum diagnose"}, {"id": 17, "column": "cT"}, {"id": 18, "column": "cN"}, {"id": 19, "column": "cM"}, {"id": 20, "column": "PBD"}]


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
                        'Database': p["column"],
                        'column': p["column"],
                        'content': p["column"],
                        'id': p["id"],
                        'predicted': p["column"]
                    })
                print(selected_column)
        return render_template('predicted.html', posts=selected_column)

    for p in posts:
        print(p)

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

