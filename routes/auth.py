import requests, json
import jwt, datetime
from flask import Flask, Blueprint, url_for, session
from flask import jsonify, request, Response, abort
from flask import render_template, redirect
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_raw_jwt
# from flask_restplus import abort

from database import db
from models.User import User, UserSchema

auth = Blueprint('auth', __name__)

blacklist = set()

redirect_uri = "http://localhost:8080/investment"
client_id = "1654259982"
client_secret = "0f39cf55ed96aa82b4f101fcbe2e7649"

# @auth.errorhandler(401)
# def resource_not_found(e):
#     return jsonify(error=str(e)), 401

@auth.route("/auth/line/login_url", methods=["GET"])
def getLineLoginURL():
  # CSRF = Math.random().toString(36).slice(2)
  loginURL = ("https://access.line.me/oauth2/v2.1/authorize?response_type=code"
        "&client_id=1654259982"
        "&redirect_uri=http://localhost:8080/investment"
        "&state=12313154"
        "&scope=profile%20openid%20email")

  return jsonify({
            "status": 200,
            "LineloginURL": loginURL
          }), 200

@auth.route("/auth/line/<code>", methods=["POST"])
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
      print(res)

      if (res):
        return jsonify({
            "status": "Success",
            "data": res
        }), 200
      else:
        return jsonify({
            "description": "No res"
        }), 404
    except:
      return jsonify({
          "description": "Server Error."
      }), 500
  else:
    return jsonify({
        "description": "Error."
    }), 400

@auth.route("/auth/regist", methods=["POST"])
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
          "description": "Server Error."
      }), 500

@auth.route("/auth/login", methods=["POST"])
def login():
  try:
    u_email = request.json["email"]
    u_pwd = request.json["password"]
    obj_user = User.query.filter_by(email=u_email).first()
    user_schema = UserSchema()
    user = user_schema.dump(obj_user)
    if not user:
      # abort(401, description="Email invalid")
      return jsonify({
          "description": "Email invalid."
      }), 401
    elif user["password"] != u_pwd:
      return jsonify({
          "description": "Password is wrong."
      }), 401
    else:
      expires = datetime.timedelta(days = 90)
      access_token = create_access_token(
        identity={"uid": user["uid"], "email":  user["email"]},
        expires_delta = expires)
      return jsonify({
          "status": 200,
          "access_token": access_token,
          "uid": user["uid"],
          "description": "Login success."
      }), 200
  except Exception as e:
    print(e)
    return jsonify({
          "description": "Server Error."
      }), 500
