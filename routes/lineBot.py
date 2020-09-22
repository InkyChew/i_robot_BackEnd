import requests, json, random
from flask import Flask, Blueprint, jsonify, request
from database import db
from models.User import User, UserSchema

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction, PostbackAction
from linebot.exceptions import LineBotApiError, InvalidSignatureError

lineBot = Blueprint("lineBot", __name__)

channel_access_token = "Jgvbc2trwJ0GGnbfXrYH29NeIQhr0JWuP/D72feKT6kkbw8qbakCSxt461ZguJuCutpOGUBVZ4s36FIpaThB1YvVQBC82pguJ1FMAsLQVTtlZ25Lc7RShaFgYu93LEm5VvqF9mbNgoTE4mev2RlxIAdB04t89/1O/w1cDnyilFU="
channel_secret = "1252c2b560ea5a8ff78d852764e351ec"

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@lineBot.route("/lineBot/setRichMenu", methods=["get"])
def setRichMenu():
  try:
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=843),
        selected=False,
        name="用愛發財",
        chat_bar_text="用愛發財選單",
        areas=[
          RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
            action=PostbackAction(
                    label='history',
                    display_text='查看投資歷史績效',
                    data='action=history&itemid=1'
                )
          ),
          RichMenuArea(
            bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
            action=URIAction(label="Go to Investment", uri="http://192.168.43.19:8080/auth")
          ),
          RichMenuArea(
            bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
            action=URIAction(label="Go to line.me", uri="https://line.me")
          )
        ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    content_type = "image/png"
    with open("./images/richmenu.jpg", "rb") as f:
      print(f)
      line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)
    line_bot_api.set_default_rich_menu(rich_menu_id)
    return jsonify({
            "id": rich_menu_id,
            "description": "richMenu setted."
        }), 200
  except Exception as e:
    print(e)
    return jsonify({
          "description": "Server Error."
      }), 500

@lineBot.route("/lineBot/loginMsg", methods=["POST"])
def pushLoginMsg():
  try:
    uid = request.data
    obj_user = User.query.filter_by(uid=uid).first()
    user_schema = UserSchema()
    user = user_schema.dump(obj_user)
    line_bot_api.push_message(user["lineId"], TextSendMessage(text="您已成功登入用愛發財!"))
    line_bot_api.push_message(user["lineId"], StickerSendMessage(package_id=11537, sticker_id=52002734))
    return jsonify({
          "description": "msg success"
      }), 200
  except LineBotApiError as e:
    print(e)
    return jsonify({
          "description": e
      }), 404

@lineBot.route("/lineBot/sendCode", methods=["POST"])
def sendVerifyCode():
  try:
    uid = request.data
    obj_user = User.query.filter_by(uid=uid).first()
    user_schema = UserSchema()
    user = user_schema.dump(obj_user)
    global verifyCode
    verifyCode = ""
    for i in range(4):
      code = random.randrange(0,9)
      verifyCode =  verifyCode + str(code)
    text = "請輸入驗證碼" + verifyCode
    line_bot_api.push_message(user["lineId"], TextSendMessage(text=text))
    return jsonify({
          "description": "msg success"
      }), 200
  except LineBotApiError as e:
    print(e)
    return jsonify({
          "description": e
      }), 404

@lineBot.route("/lineBot/verifyCode", methods=["POST"])
def verifyDepositCode():
  try:
    global verifyCode
    codes = request.data.decode()
    if (codes == verifyCode):
      return jsonify({
            "description": "驗證成功"
        }), 200
    else:
      print(type(codes))
      print(type(verifyCode))
      return jsonify({
          "description": "驗證碼錯誤，請重新輸入"
      }), 404
  except LineBotApiError as e:
    print(e)
    return jsonify({
          "description": e
      }), 404

@lineBot.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
      print(e)
      return jsonify({
            "description": e
        }), 404
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
