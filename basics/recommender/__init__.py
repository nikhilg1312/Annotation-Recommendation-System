from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'cb8ad7e4ed31f5f27ca78e508b38c523'


from recommender import routes