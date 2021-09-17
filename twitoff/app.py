from flask import Flask
from os import getenv
# after template folder and html file created, do render template
from flask import render_template
from flask import request
# add the following line
from .models import db, User
from .twitter import get_user_and_Tweet
from .predict import predict_user

def create_app():

    app = Flask(__name__)

    # change from, app.config["SQLALCHEMY_DATABASE_URI"] = database, to the following
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route("/")
    @app.route("/", methods=["GET", "POST"])
    def home():
        name = request.form.get("name")
        
        if name:
            get_user_and_Tweet(name)
            # user = User(name=name)
            # db.session.add(user)
            # db.session.commit()

        users = User.query.all()
        return render_template("home.html", users=users)


    @app.route("/about")
    def about():
      return "<p>This is the best app ever!</p>"

    @app.route("/refresh")
    def reresh():
      db.drop_all()
      db.create_all()
      return 'database refresh'
    
    @app.route('/predict') 
    def predict():
      user0="Kingstontech"
      user1="HyperX"
      hypo_tweet="I hate the weather today"
      prediction=predict_user(user0, user1, hypo_tweet)
      message = '"{}" is more likely to be said by @{} than @{}'.format(
                hypo_tweet, user0 if prediction else user1,
                user1 if prediction else user0)
      return message
    return app