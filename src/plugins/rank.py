from nonebot import on_command, CommandSession
from buu.aff import get_aff_list
from buu.user import User

@on_command('rank', only_to_me=False)
async def rank(session: CommandSession):
    users = list(map(lambda x: User(*x), get_aff_list()))
    if session.state['type'] == 'rank':
        users.sort(key=lambda x: x.data['total'], reverse=True)
        users = users[0: session.state['num']]
        if len(users) > 10:
            await session.send('太长了，给👴爪巴。')
        else:
            await session.send('\n'.join([user.description() for user in users]))
    elif session.state['type'] == 'id':
        print(session.state['name'])
        await session.send('\n'.join([i.description() for i in users if i.name.lower() in session.state['name']]) or 'No such user')
    else:
        session.finish('usage: /rank {num}|id:{id}|{id}')

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
    session.state['type'] = 'id'
    session.state['name'] = [x.strip().lower() for x in stripped_arg.split(',')]
