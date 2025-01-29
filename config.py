import sys
import os
import pymongo
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration
)
from map import FeatureStatus

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Config(metaclass=Singleton):
    def __init__(self):
        self.CHANNEL_SECRET = os.getenv('CHANNEL_SECRET', None)
        self.CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN', None)
        self.MONGODB_URI = os.getenv('MONGODB_URI', None)
        self.GPT_API_KEY = os.getenv('GPT_API_KEY', None)
        self.check_env()
        self.line_bot_init()
        self.feature_init()

    def check_env(self):
        """確認環境變數是否正確設定"""
        if self.CHANNEL_SECRET is None or self.CHANNEL_ACCESS_TOKEN is None:
            print("Please set LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN environment variables.")
            sys.exit(1)
        
        if self.MONGODB_URI is None:
            print("Please set MONGODB_URI environment variables.")
            sys.exit(1)

        if self.GPT_API_KEY is None:
            print("Please set GPT_API_KEY environment variables.")
            sys.exit(1)

    def line_bot_init(self):
        """初始化LINE Bot相關物件"""
        self.handler = WebhookHandler(self.CHANNEL_SECRET)
        self.configuration = Configuration(access_token=self.CHANNEL_ACCESS_TOKEN)
        self.dbclient = pymongo.MongoClient(self.MONGODB_URI)
    
    def feature_init(self):
        self.feature = {
            'menu': FeatureStatus.ENABLE,
            '魔法盒子機器人': FeatureStatus.ENABLE,
            '1A2B': FeatureStatus.ENABLE,
            '行事曆': FeatureStatus.ENABLE,
            '猜拳': FeatureStatus.ENABLE,
        }