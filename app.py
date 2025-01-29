from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import *
from linebot.v3.messaging import *
from linebot_helper import LineBotHelper, RichMenuHelper, DatetimeHelper
from map import MAP
from features.menu import menu
from features.ai_bot import handle_gpt_request, choose_reply
from features.fist import create_user_fist_quick_reply, handle_fist
from features.guess_number import handle_guess_number, create_system_guess_number, create_guess_quick_reply
from features.calendar import get_datetime_quick_reply
from datetime import datetime
import mongodb
import os

app = Flask(__name__)

if mongodb.get_dbclient():
    print("Connected to MongoDB.")
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
    
    mongodb.update_user_status(user_id, "active", datetime.now(), user_info.display_name)
    
    # 使用 TextMessage 創建消息
    message = TextMessage(text=f"歡迎【{user_info.display_name}】加入我的魔法盒子!")
    
    # 調用 LineBotHelper.reply_message 方法
    LineBotHelper.reply_message(event, [message])  # 傳入一個包含消息物件的列表

@line_handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    mongodb.update_user_status(user_id, "inactive", datetime.now())

@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        user_message = event.message.text

        # 根據使用者的輸入更新狀態或執行對應功能
        if user_message in MAP.FEATURE:
            feature = MAP.FEATURE[user_message]
            if feature != "1A2B":
                mongodb.delete_user_answer(user_id)
            if feature == "menu":
                menu(event)
                return

            elif feature == "magicBoxBot":
                mongodb.write_user_func(user_id, "magicBoxBot")
                messages = choose_reply(event)
                LineBotHelper.reply_message(event, messages)

            elif feature == "1A2B":
                mongodb.write_user_answer(user_id, create_system_guess_number())
                mongodb.write_user_func(user_id, "1A2B")
                messages = [TextMessage(text="開始 1A2B 遊戲！請輸入你的第一個猜測。")]
                LineBotHelper.reply_message(event, messages)

            elif feature == "calendar":
                mongodb.write_user_func(user_id, "calendar")
                messages = get_datetime_quick_reply(event)
                return LineBotHelper.reply_message(event, messages)

            elif feature == "paper_scissor_stone":
                mongodb.write_user_func(user_id, "paper_scissor_stone")
                messages = create_user_fist_quick_reply(event, "請出拳：")
                LineBotHelper.reply_message(event, messages)

        else:
            user_func = mongodb.get_user_func(user_id)
            if user_func.get("func") == "magicBoxBot":
                user_input = event.message.text
                bot_reply = handle_gpt_request(event, user_input)
                mongodb.delete_user_func(user_id)
                return LineBotHelper.reply_message(event, bot_reply)

            # 根據當前的狀態進行操作
            elif user_func.get("func") == "1A2B":
                # 進行 1A2B 遊戲
                user_guess = user_message
                answer = mongodb.get_user_answer(user_id)
                result_message, status = handle_guess_number(event, user_guess, answer)
                if status == "continue":
                    messages = create_guess_quick_reply(event, result_message)
                    return LineBotHelper.reply_message(event, messages)
                elif status == "win":
                    messages = [TextMessage(text=result_message)]
                    mongodb.delete_user_func(user_id)
                    mongodb.delete_user_answer(user_id)
                    return LineBotHelper.reply_message(event, messages)
                else:
                    return
            
            elif user_func.get("func") == "calendar":
                if user_func.get("data"):
                    selected_time = user_func.get("data").get("datetime")
                    user_message = event.message.text
                    mongodb.write_user_calendar(user_id, selected_time, user_message)
                    mongodb.delete_user_func(user_id)
                    messages = [TextMessage(text="日期已記錄！")]
                    return LineBotHelper.reply_message(event, messages)
                else:
                    return

            elif user_func.get("func") == "paper_scissor_stone":
                if user_message in ['剪刀', '石頭', '布']:
                    user_fist = user_message
                    result = handle_fist(user_fist)
                    messages = [TextMessage(text=result)]
                    mongodb.delete_user_func(user_id)
                    return LineBotHelper.reply_message(event, messages)
                else:
                    messages = create_user_fist_quick_reply(event, "輸入不符合規則，請重新輸入。")
                    return LineBotHelper.reply_message(event, messages)

            elif '魔法盒' in user_message or '魔法盒子' in user_message:
                mongodb.write_user_func(user_id, "magicBoxBot")
                messages = choose_reply(event)
                return LineBotHelper.reply_message(event, messages)

            else:
                mongodb.delete_user_func(user_id)
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

            if feature != "1A2B":
                mongodb.delete_user_answer(user_id)

            if feature == "menu":
                menu(event)
                return

            elif feature == "magicBoxBot":
                mongodb.write_user_func(user_id, "magicBoxBot")
                if params.get('text'):
                    messages = handle_gpt_request(event, params.get('text'))
                    mongodb.delete_user_func(user_id)
                    return LineBotHelper.reply_message(event, messages)
                else:
                    mongodb.write_user_func(user_id, "magicBoxBot")
                    messages = choose_reply(event)
                    return LineBotHelper.reply_message(event, messages)

            elif feature == "1A2B":
                mongodb.write_user_func(user_id, "1A2B")
                if params.get('status') == "leave":
                    mongodb.delete_user_func(user_id)
                    mongodb.delete_user_answer(user_id)
                    messages = [TextMessage(text="退出 1A2B 遊戲！")]
                    return LineBotHelper.reply_message(event, messages)
                else:
                    mongodb.write_user_answer(user_id, create_system_guess_number())
                    messages = create_guess_quick_reply(event, "請輸入你的猜測或選擇以下功能：")
                    return LineBotHelper.reply_message(event, messages)

            elif feature == "calendar":
                mongodb.write_user_func(user_id, "calendar")
                if params.get('type') == "datetime":
                    datetime = params.get('datetime')
                    data = {"datetime": datetime}
                    mongodb.update_user_func(user_id, "calendar", data)
                    date, time = DatetimeHelper.handle_datetime(datetime)
                    messages = [TextMessage(text=f"您選擇的日期為：{date}，時間為：{time}，請紀錄資訊：")]
                    return LineBotHelper.reply_message(event, messages)
                elif params.get('type') == "search":
                    user_records = mongodb.get_user_calendar(user_id)
                    if user_records:
                        merged_text = ""
                        for i, user_record in enumerate(user_records):
                            date, time = DatetimeHelper.handle_datetime(user_record['datetime'])
                            input_text = user_record['case']
                            message = f"日期：{date}\n時間：{time}\n紀錄：{input_text}"
                            if i < len(user_records) - 1:
                                merged_text += "\n"
                            merged_text += message
                            messages = [TextMessage(text=merged_text)]
                            return LineBotHelper.reply_message(event, messages)
                    else:
                        messages = [TextMessage(text="您尚未記錄日期。")]
                        mongodb.delete_user_func(user_id)
                        return LineBotHelper.reply_message(event, messages)
                elif params.get('status') == "leave":
                    mongodb.delete_user_func(user_id)
                    messages = [TextMessage(text="退出行事曆功能！")]
                    return LineBotHelper.reply_message(event, messages)
                else:
                    mongodb.write_user_func(user_id, "calendar")
                    messages = get_datetime_quick_reply(event)
                    return LineBotHelper.reply_message(event, messages)

            elif feature == "paper_scissor_stone":
                mongodb.write_user_func(user_id, "paper_scissor_stone")
                if params.get('fist'):
                    user_fist = params.get('fist')
                    result = handle_fist(user_fist)
                    messages = [TextMessage(text=result)]
                    mongodb.delete_user_func(user_id)
                    return LineBotHelper.reply_message(event, messages)
                else:
                    messages = create_user_fist_quick_reply(event, "請出拳：")
                    return LineBotHelper.reply_message(event, messages)
            else:
                mongodb.delete_user_func(user_id)
                mongodb.delete_user_answer(user_id)
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