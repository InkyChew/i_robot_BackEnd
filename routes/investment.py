import requests, json
from flask import Flask, Blueprint, jsonify, request
from database import db
from models.User import User, UserSchema

investment = Blueprint("investment", __name__)

@investment.route("/investment/sendCode", methods=["post"])
def sendCode(): # 立即投資發送驗證碼至line
  try:
    return jsonify({
          "description": "richMenu setted."
      }), 200
  except Exception as e:
    print(e)
    return jsonify({
          "description": "Server Error."
      }), 500

@investment.route("/investment/setRichMenu", methods=["get"])
def verifyCode(): # 確認驗證碼符合，傳送匯款成功至line
  try:
    return jsonify({
          "description": "richMenu setted."
      }), 200
  except Exception as e:
    print(e)
    return jsonify({
          "description": "Server Error."
      }), 500
