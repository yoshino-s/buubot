import requests
from .session import s
import bs4
import re
from . import cache

r = re.compile('<a href="\/users\/(\d+)">\W+([^\n\t]+)\W+<\/a>')

def _get_aff_list(name='V&N', category='all'):
    l = []
    idx = 0
    while True:
        idx+=1
        t = s.get(f'https://buuoj.cn/scoreboard', params = {
            'affiliation': name,
            'category': category,
            'page': idx
        }).text
        res = r.findall(t)
        if not res:
            break
        l += res
    print(len(l))
    return l

def get_aff_list(name=['V&N','/r'], category='all'):
    if type(name)==str:
        return cache.get_cache(f'cache_{name}_{category}', lambda: _get_aff_list(name, category), 60 * 60 * 24)
    else:
        l = []
        for i in name:
            l += cache.get_cache(f'cache_{i}_{category}', lambda: _get_aff_list(i, category), 60 * 60 * 24)
        return l