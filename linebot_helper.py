from flask import Flask, request, abort, url_for
from linebot.v3.webhooks import *
from linebot.v3.messaging import *
from config import Config
import json

config = Config()
configuration = config.configuration

class LineBotHelper:
    @staticmethod
    def reply_message(event, messages):
        # 確保 messages 是列表，且包裝為 TextMessage
        if not isinstance(messages, list):
            messages = [messages]

        messages = [TextMessage(text=msg) if isinstance(msg, str) else msg for msg in messages]

        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )

    @staticmethod
    def create_action(action: dict):
        """Returns
        Action: action 物件
        """
        action_type = action.get('type')
        if not action_type:
            raise ValueError("Action type is required in the action dictionary.")

        action_creators = {
            'uri': lambda a: URIAction(uri=a.get('uri', '')),
            'message': lambda a: MessageAction(text=a.get('text', ''), label=a.get('label', '')),
            'postback': lambda a: PostbackAction(data=a.get('data', ''), label=a.get('label', ''), display_text=a.get('displayText', '')),
            'datetimepicker': lambda a: DatetimePickerAction(type=a.get('type', ''), label=a.get('label', ''), data=a.get('data', ''), mode=a.get('mode', '')),
            'richmenuswitch': lambda a: RichMenuSwitchAction(
                rich_menu_alias_id=a.get('richMenuAliasId', ''),
                data=a.get('data', '')
            )
        }

        if action_type in action_creators:
            return action_creators[action_type](action)
        else:
            raise ValueError(f'Invalid action type: {action_type}')
    
    @staticmethod
    def play_animation(event):
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.show_loading_animation(
                ShowLoadingAnimationRequest(
                    chatId=event.source.user_id,
                    loadingSeconds=10
                )
            )
    
    @staticmethod
    def get_image_url(path):
        url = request.url_root[:-1]
        img_path = path
        image_url = url + url_for('static', filename=img_path)
        image_url = image_url.replace('http://', 'https://')
        return image_url

class QuickReplyHelper:
    @staticmethod
    def create_quick_reply(quick_reply_data: list[dict]):
        """Returns
        QuickReply: 快速回覆選項
        """
        return QuickReply(
            items=[QuickReplyItem(action=LineBotHelper.create_action(json.loads(item))) for item in quick_reply_data]
        )

class RichMenuHelper:
    def create_rich_menu_():
        try:
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_blob_api = MessagingApiBlob(api_client)
                areas = [
                    RichMenuArea(
                        bounds=RichMenuBounds(
                            x=0,
                            y=0,
                            width=1200,
                            height=405
                        ),
                        action=PostbackAction(data="feature=menu", label="主選單", display_text="主選單")
                    )
                ]

                rich_menu_to_create = RichMenuRequest(
                    size=RichMenuSize(
                        width=1200,
                        height=405
                    ),
                    selected=True,
                    name="主選單",
                    chat_bar_text="點擊開啟選單",
                    areas=areas
                )

                response = line_bot_api.create_rich_menu(
                    rich_menu_request=rich_menu_to_create
                )
                rich_menu_id = response.rich_menu_id
                print(f"Rich Menu 已建立，ID: {rich_menu_id}")

                image_path = './static/richmenu/richmenu.png'
                with open(image_path, 'rb') as image:
                    line_bot_blob_api.set_rich_menu_image(
                        rich_menu_id=rich_menu_id,
                        body=bytearray(image.read()),
                        _headers={'Content-Type': 'image/png'}
                    )
                print("Rich Menu 圖片已成功上傳")

                line_bot_api.set_default_rich_menu(rich_menu_id)
                print("Rich Menu 已設為預設選單")

                return rich_menu_id
        except Exception as e:
            print(f"建立 Rich Menu 時發生錯誤：{e}")
            return None

class DatetimeHelper:
    @staticmethod
    def handle_datetime(datetime):
        datetime = datetime.split("T")
        date = datetime[0]
        time = datetime[1]
        return date, time
        