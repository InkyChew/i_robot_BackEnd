import requests, json
import jwt
from flask import Flask, url_for, session
from flask import jsonify, request
from flask import render_template, redirect
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from models.User import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/stockai'
# db = SQLAlchemy()

redirect_uri = "http://localhost:8080/investment"
client_id = "1654259982"
client_secret = "0f39cf55ed96aa82b4f101fcbe2e7649"


db.init_app(app)

@app.route("/auth/line/login_url", methods=["GET"])
def getLineLoginURL():
  # CSRF = Math.random().toString(36).slice(2)
  loginURL = ("https://access.line.me/oauth2/v2.1/authorize?response_type=code"
        "&client_id=1654259982"
        "&redirect_uri=http://localhost:8080/investment"
        "&state=12313154"
        "&scope=profile%20openid%20email")

  return jsonify({
            "status": "Success",
            "LineloginURL": loginURL
          }), 200

@app.route("/auth/line/<code>", methods=["POST"])
def postCodeToLine(code):

  if (code):
    try:
      headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
      body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
      }
      lineAPI = "https://api.line.me/oauth2/v2.1/token"

      res = requests.post(lineAPI, headers=headers, data=body)
      # 解碼id_token取得使用者資訊      
      # idTokenDecode = jwt.decode(res.id_token,
      #                         client_secret,
      #                         audience=client_id,
      #                         issuer='https://access.line.me',
      #                         algorithms=['HS256'])
      # print(idTokenDecode)

      if (res):
        return jsonify({
            "status": "Success",
            "data": res
        }), 200
      else:
        return jsonify({
            "status": "Error",
            "description": "No res"
        }), 404
    except:
      return jsonify({
          "status": "Error",
          "description": "Server Error."
      }), 500
  else:
    return jsonify({
        "status": "Error",
        "description": "Error."
    }), 400

@app.route("/auth/regist", methods=["POST"])
def postNewUser():
  try:
    email = request.json["email"]
    password = request.json["password"]
    name = request.json["name"]

    newUser = User(email, password, name)
    db.session.add(newUser)
    db.session.commit()
    return jsonify({
            "status": "Success",
            "data": {
              "name": name
            }
        }), 200
  except:
    return jsonify({
          "status": "Error",
          "description": "Server Error."
      }), 500

@app.route('/')
def index():
    # Create all tables
    db.create_all()
    return 'ok'

if __name__ == "__main__":
    CORS(app)
    app.run(host="localhost", port=8888)
