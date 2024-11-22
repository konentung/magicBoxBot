from linebot.v3.models import *
from linebot.v3.messaging import *
from linebot_helper import LineBotHelper
import json

def menu(event):
    line_flex_json = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": LineBotHelper.get_image_url("mainMenu/menu.png"),
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "https://line.me/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "魔法盒子",
                    "size": "xl",
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": LineBotHelper.get_image_url("mainMenu/robot.png")
                                },
                                {
                                    "type": "text",
                                    "text": "GPT機器人",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "聊天嗎",
                                    "size": "sm",
                                    "align": "end",
                                    "color": "#aaaaaa"
                                }
                            ],
                            "action": {
                                "type": "postback",
                                "label": "來和機器人聊天吧",
                                "data": "feature=魔法盒子機器人"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": LineBotHelper.get_image_url("mainMenu/1A2B.png")
                                },
                                {
                                    "type": "text",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0,
                                    "text": "1A2B"
                                },
                                {
                                    "type": "text",
                                    "text": "來猜吧",
                                    "size": "sm",
                                    "align": "end",
                                    "color": "#aaaaaa"
                                }
                            ],
                            "action": {
                                "type": "postback",
                                "label": "猜數字啦",
                                "data": "feature=1A2B"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": LineBotHelper.get_image_url("mainMenu/rock_paper_scissors.png")
                                },
                                {
                                    "type": "text",
                                    "text": "猜拳機器人",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "賭賭看",
                                    "size": "sm",
                                    "align": "end",
                                    "color": "#aaaaaa"
                                }
                            ],
                            "action": {
                                "type": "postback",
                                "label": "猜拳吧",
                                "data": "feature=猜拳"
                            }
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "contents": [
                                {
                                    "type": "icon",
                                    "url": LineBotHelper.get_image_url("mainMenu/calander.png")
                                },
                                {
                                    "type": "text",
                                    "text": "日曆",
                                    "weight": "bold",
                                    "margin": "sm",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "小記錄",
                                    "size": "sm",
                                    "align": "end",
                                    "color": "#aaaaaa"
                                }
                            ],
                            "action": {
                                "type": "postback",
                                "label": "日曆",
                                "data": "feature=行事曆"
                            }
                        }
                    ],
                    "spacing": "md"
                }
            ],
            "spacing": "md"
        }
    }
    line_flex_str = json.dumps(line_flex_json)
    LineBotHelper.reply_message(event, [FlexMessage(alt_text="menu", contents=FlexContainer.from_json(line_flex_str))])