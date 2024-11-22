from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import *
from linebot.v3.messaging import *
from linebot_helper import LineBotHelper, RichMenuHelper
from map import MAP
from features.menu import menu
from features.ai_bot import handle_gpt_request, choose_reply
from features.fist import create_user_fist_quick_reply, handle_fist
from features.guess_number import handle_guess_number, create_system_guess_number, create_guess_quick_reply
from features.calendar import get_datetime_quick_reply, get_user_record, update_user_record, handle_datetime
from collections import defaultdict
import random
import os
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
GPT_API_KEY = os.getenv("GPT_API_KEY")
    
line_handler = WebhookHandler(CHANNEL_SECRET)

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_info = line_bot_api.get_profile(user_id)
    
    # 使用 TextMessage 創建消息
    message = TextMessage(text=f"歡迎【{user_info.display_name}】加入我的魔法盒子!")
    
    # 調用 LineBotHelper.reply_message 方法
    LineBotHelper.reply_message(event, [message])  # 傳入一個包含消息物件的列表

# 建立一個字典來維護每個使用者的狀態
user_states = defaultdict(dict)

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        user_message = event.message.text

        # 取得使用者當前的狀態
        user_state = user_states.get(user_id, {"stage": "default"})

        # 根據使用者的輸入更新狀態或執行對應功能
        if user_message in MAP.FEATURE:
            feature = MAP.FEATURE[user_message]
            if feature == "menu":
                menu(event)
                user_states[user_id] = {"stage": "default"}

            elif feature == "magicBoxBot":
                user_states[user_id] = {"stage": "magic_box_bot"}
                messages = choose_reply(event)
                LineBotHelper.reply_message(event, messages)

            elif feature == "1A2B":
                answer = create_system_guess_number()
                user_states[user_id] = {"stage": "1A2B", "game_state": "init", "answer": answer}
                messages = [TextMessage(text="開始 1A2B 遊戲！請輸入你的第一個猜測。")]
                LineBotHelper.reply_message(event, messages)

            elif feature == "calendar":
                user_states[user_id] = {"stage": "calendar"}
                messages = get_datetime_quick_reply(event)
                return LineBotHelper.reply_message(event, messages)

            elif feature == "paper_scissor_stone":
                user_states[user_id] = {"stage": "paper_scissor_stone"}
                messages = create_user_fist_quick_reply(event, "請出拳：")
                LineBotHelper.reply_message(event, messages)

        else:
            if user_state["stage"] == "magic_box_bot":
                user_input = event.message.text
                bot_reply = handle_gpt_request(event, user_input)
                user_states[user_id] = {"stage": "default"}
                return LineBotHelper.reply_message(event, bot_reply)

            # 根據當前的狀態進行操作
            elif user_state["stage"] == "1A2B":
                # 進行 1A2B 遊戲
                user_guess = user_message
                answer = user_state["answer"]
                result_message, status = handle_guess_number(event, user_guess, answer)
                if status == "continue":
                    messages = create_guess_quick_reply(event, result_message)
                    return LineBotHelper.reply_message(event, messages)
                elif status == "win":
                    messages = [TextMessage(text=result_message)]
                    user_states[user_id] = {"stage": "default"}
                    return LineBotHelper.reply_message(event, messages)
                else:
                    return
            
            elif user_state["stage"] == "calendar":
                if user_states[user_id].get("datetime"):
                    selected_time = user_states[user_id].get("datetime")
                    user_message = event.message.text
                    update_user_record(user_id, selected_time, user_message)
                    user_states[user_id] = {"stage": "default"}
                    messages = [TextMessage(text="日期已記錄！")]
                    return LineBotHelper.reply_message(event, messages)
                else:
                    return

            elif user_state["stage"] == "paper_scissor_stone":
                if user_message in ['剪刀', '石頭', '布']:
                    user_fist = user_message
                    result = handle_fist(user_fist)
                    messages = [TextMessage(text=result)]
                    user_states[user_id] = {"stage": "default"}
                    return LineBotHelper.reply_message(event, messages)
                else:
                    user_states[user_id] = {"stage": "paper_scissor_stone"}
                    messages = create_user_fist_quick_reply(event, "輸入不符合規則，請重新輸入。")
                    return LineBotHelper.reply_message(event, messages)

            elif '魔法盒' in user_message or '魔法盒子' in user_message:
                user_states[user_id] = {"stage": "magic_box_bot"}
                messages = choose_reply(event)
                LineBotHelper.reply_message(event, messages)

            else:
                return LineBotHelper.reply_message(event, [TextMessage(text="無此功能")])

    except Exception as e:
        app.logger.error(f"發生錯誤：{e}")
        LineBotHelper.reply_message(event, [TextMessage(text='發生錯誤，請聯繫系統管理員！')])

@line_handler.add(PostbackEvent)
def handle_postback(event):
    try:
        user_id = event.source.user_id
        postback_data = event.postback.data
        postback_params = event.postback.params
        params = postback_params if postback_params else {}
        if '=' in postback_data:
            # 重新拆解Postback Data的參數
            for param in postback_data.split('&'):
                key, value = param.split('=')
                params[key] = value
        feature = params.get('feature') if params.get('feature') else postback_data
        if feature in MAP.FEATURE:
            feature = MAP.FEATURE[feature]

            if feature == "menu":
                menu(event)
                user_states[user_id] = {"stage": "default"}
                return

            elif feature == "magicBoxBot":
                if params.get('text'):
                    user_states[user_id] = {"stage": "magic_box_bot"}
                    messages = handle_gpt_request(event, params.get('text'))
                    user_states[user_id] = {"stage": "default"}
                    return LineBotHelper.reply_message(event, messages)
                else:
                    user_states[user_id] = {"stage": "magic_box_bot"}
                    messages = choose_reply(event)
                    return LineBotHelper.reply_message(event, messages)

            elif feature == "1A2B":
                if params.get('status') == "leave":
                    user_states[user_id] = {"stage": "default"}
                    messages = [TextMessage(text="退出 1A2B 遊戲！")]
                    return LineBotHelper.reply_message(event, messages)
                else:
                    answer = create_system_guess_number()
                    user_states[user_id] = {"stage": "1A2B", "game_state": "init", "answer": answer}
                    messages = create_guess_quick_reply(event, "請輸入你的猜測或選擇以下功能：")
                    return LineBotHelper.reply_message(event, messages)

            elif feature == "calendar":
                if params.get('type') == "datetime":
                    datetime = params.get('datetime')
                    user_states[user_id] = {"stage": "calendar", "datetime": datetime}
                    date, time = handle_datetime(datetime)
                    messages = [TextMessage(text=f"您選擇的日期為：{date}，時間為：{time}，請紀錄資訊：")]
                    return LineBotHelper.reply_message(event, messages)
                elif params.get('type') == "search":
                    user_record = get_user_record(user_id)
                    if user_record:
                        date, time = handle_datetime(user_record['time'])
                        messages = [TextMessage(text=f"您的日期為：{date}\n您的時間為：{time}\n您的紀錄為：{user_record['input']}")]
                    else:
                        messages = [TextMessage(text="您尚未記錄日期。")]
                    user_states[user_id] = {"stage": "default"}
                    return LineBotHelper.reply_message(event, messages)
                elif params.get('status') == "leave":
                    user_states[user_id] = {"stage": "default"}
                    messages = [TextMessage(text="退出行事曆功能！")]
                    return LineBotHelper.reply_message(event, messages)
                else:
                    user_states[user_id] = {"stage": "calendar"}
                    messages = get_datetime_quick_reply(event)
                    return LineBotHelper.reply_message(event, messages)

            elif feature == "paper_scissor_stone":
                if params.get('fist'):
                    user_fist = params.get('fist')
                    result = handle_fist(user_fist)
                    messages = [TextMessage(text=result)]
                    user_states[user_id] = {"stage": "default"}
                    return LineBotHelper.reply_message(event, messages)
                else:
                    user_states[user_id] = {"stage": "paper_scissor_stone"}
                    messages = create_user_fist_quick_reply(event, "請出拳：")
                    return LineBotHelper.reply_message(event, messages)
            else:
                messages = [TextMessage(text="未知的功能選擇，請重新輸入。")]
                return LineBotHelper.reply_message(event, messages)

        else:
            messages = [TextMessage(text="未知的功能選擇，請重新輸入。")]
            return LineBotHelper.reply_message(event, messages)
        
    except Exception as e:
        app.logger.error(f"發生錯誤：{e}")
        LineBotHelper.reply_message(event, [TextMessage(text='發生錯誤，請聯繫系統管理員！')])


# 需要生成richmenu時，請將下面解除註解
# RichMenuHelper.create_rich_menu_()

if __name__ == "__main__":
    app.run()