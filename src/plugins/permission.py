from nonebot import on_command, CommandSession
import nonebot

from typing import Union, Set
import json

PERMISSION_LEVEL = ['ROOT', 'ADMIN', 'NORNAL']

PERMISSION = [
    set(),
    set(),
    set()
]

cmds = ['ls', 'help', 'add', 'remove']

def load_perm():
    d = []
    try:
        with open('perm.json') as f:
            d = json.load(f)
        for i in range(2):
            PERMISSION[i] = set(d[i])
    except Exception:
        pass
load_perm()

def save_perm():
    d = [[], []]
    for i in range(2):
        d[i] = list(PERMISSION[i])
    with open('perm.json', 'w') as f:
        json.dump(d, f)

def get_permission_users(level: Union[int, str]) -> Set[str]:
    if type(level) == str:
        level = PERMISSION_LEVEL.index(level)
    return PERMISSION[level]

def get_permission(id: str) -> int:
    id = str(id)
    for (l, i) in enumerate(PERMISSION):
        if id in i:
            return l
    return 2

def check_permission(id: str, level: Union[int, str]) -> bool:
    id = str(id)
    if type(level) == str:
        level = PERMISSION_LEVEL.index(level)
    for (l, i) in enumerate(PERMISSION):
        if id in i:
            return l<=level

def permission(level: Union[int, str]):
    def _(func):
        def f(session: CommandSession):
            if check_permission(session.ctx['user_id'], level):
                return func(session)
            else:
                session.finish('You have no permission to execute this command.')
            return
        return f
    return _

def add_permission(id: str, level: Union[int, str]) -> int:
    id = str(id)
    if type(level) == str:
        level = PERMISSION_LEVEL.index(level)
    for (l, i) in enumerate(PERMISSION):
        if l == level:
            i.add(id)
            save_perm()
            return l
        else:
            i.discard(id)

def remove_permission(id: str) -> int:
    add_permission(id, 3)



@on_command('perm', only_to_me=False)
@permission('ADMIN')
async def status(session: CommandSession):
    global cmds
    res = '/perm '+'|'.join(cmds)
    cmd = session.state['cmd']
    args = session.state['args']
    bot = nonebot.get_bot()
    print(cmd, args)
    if cmd == 'ls':
        res = '/perm ls ROOT|ADMIN'
        if len(args) == 1 and args[0].upper() in PERMISSION_LEVEL:
            level = args[0].upper()
            res = level + ': ' + ','.join(get_permission_users(level))
    if cmd == 'add':
        res = '/perm add ROOT|ADMIN id1 id2...'
        if len(args) > 1 and args[0].upper() in PERMISSION_LEVEL:
            level = args[0].upper()
            for i in args[1:]:
                add_permission(i, level)
            res = level + ' now has: ' + ','.join(get_permission_users(level))
    await session.send(res)

@status.args_parser
async def _(session: CommandSession):
    global cmds
    cmd = 'help'
    args = []
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        splitted = stripped_arg.split(' ')
        c = splitted[0]
        if c in cmds:
            cmd = c
            args = splitted[1:]
    session.state['cmd'] = cmd
    session.state['args'] = args
