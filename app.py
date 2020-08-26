from flask import Flask
from database import db
from flask_cors import CORS
from routes.auth import auth

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/stockai'

app.register_blueprint(auth)

# db.init_app(app)

@app.route('/')
def index():
    db.init_app(app)
    db.create_all()
    return 'ok'

if __name__ == "__main__":
    CORS(app)
    # from routes.__init__ import *
    app.run(host="localhost", port=8888)