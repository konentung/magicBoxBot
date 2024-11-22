from linebot.v3.messaging import *
from linebot.v3.models import *
from openai import OpenAI
from linebot_helper import LineBotHelper, QuickReplyHelper
import random

def handle_guess_number(event, user_guess, answer):
    for i in user_guess:
        if i not in "0123456789":
            return "請輸入四位數字。", "continue"
    if len(user_guess) != 4:
        return "請輸入四位數字。", "continue"
    a = 0
    b = 0
    for i in range(4):
        if user_guess[i] == answer[i]:
            a += 1
        elif user_guess[i] in answer:
            b += 1
    if a == 4:
        return "恭喜你猜對了！", "win"
    else:
        return "{}A{}B".format(a, b), "continue"

def create_system_guess_number():
    return "".join(random.sample("0123456789", 4))

def create_guess_quick_reply(event, message):
    LineBotHelper.play_animation(event)
    quick_reply_data = [
        """{"type": "postback", "label": "退出遊戲", "data": "feature=1A2B&status=leave", "displayText": "退出遊戲"}""",
        """{"type": "postback", "label": "回主選單", "data": "feature=menu", "displayText": "主選單"}"""
    ]
    quick_reply = QuickReplyHelper.create_quick_reply(quick_reply_data=quick_reply_data)
    return TextMessage(text=message, quick_reply=quick_reply)