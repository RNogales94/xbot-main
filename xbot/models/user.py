import hashlib
from datetime import datetime
from xbot.xbotdb import Xbotdb


def create_token(user_name):
    if user_name:
        hasher = hashlib.sha256()
        hasher.update(user_name.encode())
        return hasher.hexdigest()
    else:
        return None


class User:
    """
    Examples
    telegram_name: RNogales
    telegram_channels: ['@canalejemplo', '@chollos']
    """
    def __init__(self, *args, telegramName=None, chatId=None, type='free', amazonTag=None, telegramChannels=[], referrals=[]):
        self.telegram_name = telegramName
        self.amazon_tag = amazonTag
        self.type = type
        self.telegram_channels = telegramChannels
        self.token = create_token(self.telegram_name)
        self.chat_id = chatId
        self.creation_timestamp = datetime.now().timestamp()
        self.referrals = referrals
        self.last_modify = self.creation_timestamp

    def __str__(self):
        return f'User: [{self.telegram_name}, {self.amazon_tag}, {self.telegram_channels},{self.referrals}, {self.token} ]'

    def get_telegram_name(self):
        return self.telegram_name

    def save(self):
        Xbotdb.insert_user(user=self)

    def to_dict(self):
        u = {'telegramName': self.telegram_name,
             'amazonTag': self.amazon_tag,
             'telegramChannels': self.telegram_channels,
             'referrals': self.referrals,
             'token': self.token,
             'chatId': self.chat_id,
             'creationTimestamp': self.creation_timestamp,
             'lastModify': self.last_modify,
             }
        return u
