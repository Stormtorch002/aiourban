import aiohttp
import re
from exceptions import *


_word_extractor = re.compile('[(.+?)]')
_session = aiohttp.ClientSession()
_url = 'http://api.urbandictionary.com/v0/define'


class Post:

    def __init__(self, raw):
        self.word = raw.get('word')
        self.author = raw.get('author')
        self.url = raw.get('permalink')
        self.upvotes = raw.get('thumbs_up')
        self.downvotes = raw.get('thumbs_down')
        self.id = raw.get('defid')
        self.hyperlinks = {}

        i = 0
        for word in _word_extractor.findall(raw.get('definition')):
            try:
                self.hyperlinks[word] = raw.get('sound_urls')[i]
                i += 1
            except IndexError:
                break


def _remove_brackets(text: str):
    return text.replace('[', '').replace(']', '')


async def _request(word: str):
    async with _session.get(_url, params={'term': word}) as resp:
        if resp.status == 429:
            raise TooManyRequests('You are being ratelimited.')
        if resp.status != 200:
            raise UrbanError('Something went wrong.')

        data = await resp.json()
        if not data.get('list'):
            raise TermNotFound('Search term "{}" not found.'.format(word))
        return data


async def define(word: str):
    data = await _request(word)
    return [_remove_brackets(post['definition']) for post in data]


async def get_posts(word: str):
    data = await _request(word)
    return [Post(post) for post in data['list']]
