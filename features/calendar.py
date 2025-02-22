from linebot.v3.models import *
from linebot.v3.messaging import *
from linebot_helper import LineBotHelper, QuickReplyHelper
import json
import mongodb
import os

def create_month_quick_reply(event):
    LineBotHelper.play_animation(event)
    
    month_quick_reply = [
        """{"type": "postback", "label": "一月", "data": "feature=行事曆&month=1", "displayText": "一月"}""",
        """{"type": "postback", "label": "二月", "data": "feature=行事曆&month=2", "displayText": "二月"}""",
        """{"type": "postback", "label": "三月", "data": "feature=行事曆&month=3", "displayText": "三月"}""",
        """{"type": "postback", "label": "四月", "data": "feature=行事曆&month=4", "displayText": "四月"}""",
        """{"type": "postback", "label": "五月", "data": "feature=行事曆&month=5", "displayText": "五月"}""",
        """{"type": "postback", "label": "六月", "data": "feature=行事曆&month=6", "displayText": "六月"}""",
        """{"type": "postback", "label": "七月", "data": "feature=行事曆&month=7", "displayText": "七月"}""",
        """{"type": "postback", "label": "八月", "data": "feature=行事曆&month=8", "displayText": "八月"}""",
        """{"type": "postback", "label": "九月", "data": "feature=行事曆&month=9", "displayText": "九月"}""",
        """{"type": "postback", "label": "十月", "data": "feature=行事曆&month=10", "displayText": "十月"}""",
        """{"type": "postback", "label": "十一月", "data": "feature=行事曆&month=11", "displayText": "十一月"}""",
        """{"type": "postback", "label": "十二月", "data": "feature=行事曆&month=12", "displayText": "十二月"}""",
    ]
    quick_reply = QuickReplyHelper.create_quick_reply(quick_reply_data=month_quick_reply)
    
    return TextMessage(text="請選擇月份：", quick_reply=quick_reply)

def create_days_flex(event):
    flex_json = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "日",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "一",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "二",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "三",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "四",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "五",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "六",
                    "align": "center"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                },
                {
                    "type": "image",
                    "url": "{{cover_url}}",
                    "margin": "xs",
                    "aspectMode": "cover"
                }
                ]
            }
            ]
        }
    }

def get_datetime_quick_reply(event):
    LineBotHelper.play_animation(event)
    
    datetime_quick_reply = [
        """{"type": "datetimepicker", "label": "選擇時間", "data": "feature=行事曆&type=datetime", "mode": "datetime"}""",
        """{"type": "postback", "label": "查詢日期", "data": "feature=行事曆&type=search", "displayText": "查詢日期"}""",
        """{"type": "postback", "label": "回主選單", "data": "feature=menu", "displayText": "主選單"}""",
        """{"type": "postback", "label": "退出日曆", "data": "feature=行事曆&status=leave", "displayText": "退出遊戲"}"""
        
    ]
    quick_reply = QuickReplyHelper.create_quick_reply(quick_reply_data=datetime_quick_reply)
    
    return TextMessage(text="請選擇功能：", quick_reply=quick_reply)