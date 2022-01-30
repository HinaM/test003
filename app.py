from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('9g5g2Kcs7kLA9QCH10+6u71QkX99sQ6xChHL/PhUO9z6dAVJkiWrD6VafTyTUzwvJQ+gPgLJ2u3bqpfsUST8/EiKd40wT69NaaVeBMXkfbGC+U2qSWGAaLitM6J3yaGCrhbHEehycFya5GaWlQfdVgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3d0241718c1b70a54cd33d99c0c6dc1d')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()