import pytest

from xbot.xbotdb import Xbotdb
from xbot.models.user import User

db = Xbotdb()


def test_exist_user():
    assert db.exist_user(telegram_name='RNogales') == True
    assert db.exist_user(telegram_name='hb3ejh2bd8b77c81f') == False


def test_get_user_by_chat_id():
    assert isinstance(db.get_user_by_chat_id(213337828), User)
    assert isinstance(db.get_user_by_chat_id("213337828"), User)
    assert db.get_user_by_chat_id(213337828).telegram_name == 'RNogales'
    assert db.get_user_by_chat_id("213337828").chat_id == db.get_user_by_chat_id(213337828).chat_id
    assert db.get_user_by_chat_id(23442342234234234) is None


def test_get_amazon_tag():
    assert db.get_amazon_tag(telegram_name="luiscastro193") == 'luis-21'


def test_get_telegram_channels():
    assert db.get_channels_associates(telegram_name='luiscastro193') == []


def test_get_user_type():
    assert db.get_user_type(telegram_name='luiscastro193') == 'free'

