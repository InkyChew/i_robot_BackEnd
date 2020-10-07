import json, configparser
from flask import Flask, request, abort
from database import db, ma
from flask_cors import CORS
from routes.auth import auth
from routes.lineBot import lineBot
from routes.investment import investment
from flask_jwt_extended import JWTManager
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Aaw5b5nz3@192.168.43.19/stockai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/stockai'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/stockai'

app.register_blueprint(auth)
app.register_blueprint(lineBot)
app.register_blueprint(investment)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'ga2QodlFyJiNkKjwEX_OjzSnXRNdp8UHGEVd7aP7D-FBIGHh0J6QDcDfWPQi2BV7o8MBuYheWClXf0Ue-zcaC4TDDyElQK24Yso__keiWtqKM8B0EPZmP1P5MDmfgQhrkKYFYhBmt698z4lh-H1JogfPzr69b8I3b8Rfvjv5DEdEVUlpUtKslv3ptIKTymRSXkBg4JdB7F9sll4z7G4RhocNwrPbrQv6h9GhJHIcxrmKNKCOZh0jb7280yvEFz6YajTIiAAD1Q58HUburhU1gpanswAL3mfcC5CIaMtW3w0ON2qIYR2xnypBCe2dbLh_FdZPLlWYsnpYpcyntuM_yw'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route('/')
def index():
  # db.create_all()
  print(line_bot_api)
  print(handler)
  return 'ok'

@app.route("/callback", methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature = request.headers['X-Line-Signature']

  # get request body as text
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)
  print(body)
  print(signature)
  # handle webhook body
  try:
    handler.handle(body, signature)
  except Exception as e:
    print(e)
    abort(400)

  return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  print(event)
  line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text="用AI發財 just for test"))

# @handler.add(PostbackEvent)
# def handle_postback(event):
#     if event.postback.data == 'ping':
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text='pong'))
#     elif event.postback.data == 'datetime_postback':
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
#     elif event.postback.data == 'date_postback':
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text=event.postback.params['date']))

if __name__ == "__main__":
  CORS(app)
  app.run(host="localhost", port=8888)
  # app.run(host="192.168.43.19", port=8888)