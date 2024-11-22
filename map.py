from enum import Enum, IntEnum

class FeatureStatus(Enum):
    ENABLE = 1
    DISABLE = 0

class Permission(IntEnum):
    ADMIN = 1
    USER = 2

class MAP:
    FEATURE = {
        "menu": "menu",
        "魔法盒子機器人": "magicBoxBot",
        "1A2B": "1A2B",
        "行事曆": "calendar",
        "猜拳": "paper_scissor_stone",
    }