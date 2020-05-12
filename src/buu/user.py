from .session import s
import dateutil.parser
import time, datetime
import json
from . import cache

def string2timestamp(s):
    d = dateutil.parser.parse(s)
    t = d.timetuple()
    timeStamp = int(time.mktime(t))
    timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond))/1000000
    return timeStamp

class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.update_data()
    def __str__(self):
        return f'{self.id} {self.name}'
    def update_data(self):
        self.data = self.calc(self.getDaySolves())
    def getSolves(self):
        data = cache.get_cache(self.id)
        if not data:
            print(f'Update {self.name}')
            data = s.get(f"https://buuoj.cn/api/v1/users/{self.id}/solves").json()['data']
            for i in data:
              i['date'] = string2timestamp(i['date'])
            cache.update_cache(self.id, data)
        return data
    def getDaySolves(self, cache=True):
        data = self.getSolves()
        end = time.time()
        start = end - 60 * 60 * 24
        return filter(lambda d: start <= d['date'] <= end, data)
    @staticmethod
    def calc(data):
        ret = {'total': 0, 'count': 0}
        for d in data:
            score = d['challenge']['value']
            category = d['challenge']['category'].lower()
            if not ret.get(category, 0):
                ret[category] = 0
            ret['total'] += score
            ret[category] += score
            ret['count'] += 1
        return ret
    def customSentence(self):
        data = self.data
        sentence = ''
        if data['total'] == 0:
            sentence += '我就是懒狗。'
        if data['total'] >= 600:
            sentence += '我今天大刷特刷。'
        return sentence
    def description(self):
        return f'{self.name}：今天，我做了{self.data["count"]}道，一共{self.data["total"]}分的题目。{self.customSentence()}'