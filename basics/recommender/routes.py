from flask import render_template, url_for, flash, redirect, jsonify, request
from recommender import app
from recommender.offlineDataService import get_column_names, get_selected_column, get_selected_column_post
from recommender.onlineData import insert_history_cancerdataorg

posts = get_column_names()


# [{"id": 0, "column": "Outcome"}, {"id": 1, "column": "PCI"}, {"id": 2, "column": "Geboortemaand"}, {"id": 3, "column": "Geslacht"}, {"id": 4, "column": "Invoerdatum"}, {"id": 5, "column": "VraagType"}, {"id": 6, "column": "Vraagstelling"}, {"id": 7, "column": "Antwoord"}, {"id": 8, "column": "Tumour_Treatment"}, {"id": 9, "column": "PCI"}, {"id": 10, "column": "Geboortemaand"}, {"id": 11, "column": "Geslacht"}, {"id": 12, "column": "Overleden"}, {"id": 13, "column": "Datum overlijden"}, {"id": 14, "column": "Laatste datum check in leven"}, {"id": 15, "column": "Diagnose"}, {"id": 16, "column": "Datum diagnose"}, {"id": 17, "column": "cT"}, {"id": 18, "column": "cN"}, {"id": 19, "column": "cM"}, {"id": 20, "column": "PBD"}]


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_column = get_selected_column(request.form.getlist('mycheckbox'), posts)
        return render_template('predicted.html', posts=selected_column)
    return render_template('home.html', posts=posts)


@app.route("/post/<int:post_id>", methods=['GET'])
def post(post_id):
    opted_column = get_selected_column_post(post_id, posts)
    print("in def post():", opted_column)
    return render_template('post.html', post=opted_column[0])


@app.route("/upload_history/<post_label>", methods=['POST'])
def upload_history(post_label):
    insert_history_cancerdataorg(post_label, request.form['mycheckbox'])
    return redirect(url_for('home'))


@app.route("/predicted", methods=['GET', 'POST'])
def predicted():
    print(request.form)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/multi", methods=['GET', 'POST'])
def multi():
    if request.method == 'POST':
        print(request.form.getlist('mycheckbox'))
        return 'Done'
    return render_template('multiselect.html')
