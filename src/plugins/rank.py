from nonebot import on_command, CommandSession
import requests

@on_command('rank', only_to_me=False)
async def rank(session: CommandSession):
    res = 'usage: /rank {num}|id:{id}|{id}'
    if session.state['type'] == 'rank':
        res = requests.get('https://api.yoshino-s.online/buu/official', params={
            'type': 'description',
            'limit': session.state["num"]
        }).text
    elif session.state['type'] == 'id':
        res = requests.get('https://api.yoshino-s.online/buu/search', params={
            'name': session.state["name"]
        }).json().get('message', 'Internal Error')
    print(res)
    await session.send(res)

@on_command('is_lazy_dog', only_to_me=False)
async def dog(session: CommandSession):
    res = 'usage: /is_lazy_dog id'
    res = requests.get('https://api.yoshino-s.online/buu/search', params={
        'name': session.current_arg_text.strip()
    }).json().get('message', 'Internal Error')
    await session.send(res)

@rank.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    try:
        session.state['type'] = 'rank'
        session.state['num'] = int(stripped_arg)
        return
    except Exception:
        pass
    if stripped_arg.startswith('id:'):
        try:
            session.state['type'] = 'id'
            session.state['name'] = [x.strip().lower() for x in stripped_arg[3:].split(',')]
            return
        except Exception:
            pass
    if not stripped_arg:
        session.state['type'] = 'rank'
        session.state['num'] = 3
    else:
        session.state['type'] = 'id'
        session.state['name'] = [x.strip().lower() for x in stripped_arg.split(',')]
    


@on_command('lazy_dog', only_to_me=False)
async def rank(session: CommandSession):
    res = requests.get('https://api.yoshino-s.online/buu/official', params={
            'filter': 'lazy_dog'
        }).json()
    if len(res):
        await session.send('以下为24h懒狗名单:' + ','.join(map(lambda i: i['user_name'], res)))
    else:
        await session.send('哇24h内没有懒狗。送上福利一份。')
