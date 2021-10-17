# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 15:50:24 2020

@author: jacky
"""

from flask import Flask, request, abort

from linebot.api import LineBotApi

from linebot.webhook import WebhookHandler

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('KbUSP5ShwG5gziWRdy3niYUieAZaYlDc2YMW1HB3Ao05YRm+DKUar29lK0lfqjeMqzLRm1MLALf/R4jIV/k+98YxIR40SryCI8qsokVBe31heMMafyPQSI89odk42Ts1dD9b35gyPMCkOhHEGp+M/wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b33a01e1e548c7b39a732d62245e1d36')

# 此為 Webhook callback endpoint
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body（負責）
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 決定要回傳什麼 Component 到 Channel
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == '__main__':
    app.run()