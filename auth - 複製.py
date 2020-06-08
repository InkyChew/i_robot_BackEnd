import requests, json
from flask import Flask, url_for, session
from flask import jsonify, request
from flask import render_template, redirect
from flask_cors import CORS
# from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# oauth = OAuth(app)

redirect_uri = "http://localhost:8080/"
client_id = "1654259982"
client_secret = "0f39cf55ed96aa82b4f101fcbe2e7649"

@app.route("/auth/line/login_url", methods=["GET"])
def getLineLoginURL():
  # CSRF = Math.random().toString(36).slice(2)
  loginURL = ("https://access.line.me/oauth2/v2.1/authorize?response_type=code"
        "&client_id=1654259982"
        "&redirect_uri=http://localhost:8080/"
        "&state=12313154"
        "&scope=profile%20openid%20email")

  return jsonify({
            "status": "Success",
            "LineloginURL": loginURL
          }), 200

@app.route("/auth/line", methods=["POST"])
def postCodeToLine():
  code =  request.json["code"]
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
      if (res):
        return jsonify({
            "status": "Success",
            "data": res
        }), 200
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

# oauth.register(
#     name='line',
#     client_id=client_id,
#     client_secret=client_secret,
#     access_token_url='https://api.line.me/oauth2/v2.1/token',
#     access_token_params={
#       'grant_type': 'authorization_code',
#       'redirect_uri': redirect_uri
#       },
#     authorize_url='https://access.line.me/oauth2/v2.1/authorize',
#     authorize_params={
#       'response_type': 'code',
#       'redirect_uri': redirect_uri,
#       'state': '12313154'
#       },
#     client_kwargs={'scope': 'profile%20openid%20email'},
# )

# @app.route("/auth/line/login_url", methods=["GET"])
# def getLineLoginURL():
#   redirect_uri = url_for('auth', _external=True)
#   return oauth.line.authorize_redirect(redirect_uri)

# @app.route('/auth')
# def auth():
#     token = oauth.line.authorize_access_token()
#     user = oauth.line.parse_id_token(token)
#     session['user'] = user
#     return redirect('/')

if __name__ == "__main__":
    CORS(app)
    app.run(host="localhost", port=8888)
