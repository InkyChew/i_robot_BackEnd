from flask import Flask
from database import db, ma
from flask_cors import CORS
from routes.auth import auth
from routes.lineBot import lineBot
from flask_jwt_extended import JWTManager
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Aaw5b5nz3@192.168.43.19/stockai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/stockai'

app.register_blueprint(auth)
app.register_blueprint(lineBot)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'ga2QodlFyJiNkKjwEX_OjzSnXRNdp8UHGEVd7aP7D-FBIGHh0J6QDcDfWPQi2BV7o8MBuYheWClXf0Ue-zcaC4TDDyElQK24Yso__keiWtqKM8B0EPZmP1P5MDmfgQhrkKYFYhBmt698z4lh-H1JogfPzr69b8I3b8Rfvjv5DEdEVUlpUtKslv3ptIKTymRSXkBg4JdB7F9sll4z7G4RhocNwrPbrQv6h9GhJHIcxrmKNKCOZh0jb7280yvEFz6YajTIiAAD1Q58HUburhU1gpanswAL3mfcC5CIaMtW3w0ON2qIYR2xnypBCe2dbLh_FdZPLlWYsnpYpcyntuM_yw'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)

@app.route('/')
def index():
  db.create_all()
  return 'ok'

if __name__ == "__main__":
  CORS(app)
  app.run(host="localhost", port=8888)
  # app.run(host="192.168.43.19", port=8888)