from linebot.v3.messaging import *
from linebot.v3.models import *
from openai import OpenAI
from linebot_helper import LineBotHelper, QuickReplyHelper
from config import Config

config = Config()
GPT_API_KEY = config.GPT_API_KEY


def handle_gpt_request(event, user_message):
    LineBotHelper.play_animation(event)

    client = OpenAI(api_key=GPT_API_KEY)
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個被來自台灣的魔法師創造的AI機器人，需要回答問題請使用繁體中文，你的身分是魔法盒子機器人，每個人的問題都會成為你知識的一部份，回答問題的時候可以帶有一些禮貌的字眼，希望你可以使用有趣的風格做回應，也可以偶爾使用一些表情符號為應，不要太無趣，回應的時候盡量不要用列舉的方式，使用一段短文的方式做回應，如果問到你是誰，需要使用你自己的身分做回應。"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.2
        )
        ai_reply = completion.choices[0].message.content
        return ai_reply
    except Exception as e:
        return f"發生錯誤：{e}"

def choose_reply(event):
    LineBotHelper.play_animation(event)
    quick_reply_data = [
        """{"type": "postback", "label": "請問今天早餐要吃甚麼呢?", "data": "feature=魔法盒子機器人&text=請問今天早餐要吃甚麼呢?", "displayText": "請問今天早餐要吃甚麼呢?"}""",
        """{"type": "postback", "label": "請問你是誰?", "data": "feature=魔法盒子機器人&text=請問你是誰?", "displayText": "請問你是誰?"}""",
        """{"type": "postback", "label": "更多功能", "data": "feature=menu", "displayText": "主選單"}"""
    ]

    quick_reply = QuickReplyHelper.create_quick_reply(quick_reply_data=quick_reply_data)
    
    return TextMessage(text="請選擇以下問題：", quick_reply=quick_reply)
