from linebot.v3.messaging import *
from linebot.v3.models import *
from openai import OpenAI
from linebot_helper import LineBotHelper, QuickReplyHelper
import random

def handle_fist(user_fist):
    fists = ['剪刀', '石頭', '布']
    system_fist = random.choice(fists)
    
    if user_fist == system_fist:
        return f"你出了{user_fist}，我出了{system_fist}，平手！"
    elif (user_fist == '剪刀' and system_fist == '布') or (user_fist == '石頭' and system_fist == '剪刀') or (user_fist == '布' and system_fist == '石頭'):
        return f"你出了{user_fist}，我出了{system_fist}，你贏了！"
    else:
        return f"你出了{user_fist}，我出了{system_fist}，你輸了！"

def create_user_fist_quick_reply(event, message):
    LineBotHelper.play_animation(event)
    quick_reply_data = [
        """{"type": "postback", "label": "剪刀", "data": "feature=猜拳&fist=剪刀", "displayText": "剪刀"}""",
        """{"type": "postback", "label": "石頭", "data": "feature=猜拳&fist=石頭", "displayText": "石頭"}""",
        """{"type": "postback", "label": "布", "data": "feature=猜拳&fist=布", "displayText": "布"}"""
    ]
    quick_reply = QuickReplyHelper.create_quick_reply(quick_reply_data=quick_reply_data)
    
    return TextMessage(text=message, quick_reply=quick_reply)