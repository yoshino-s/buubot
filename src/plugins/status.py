from nonebot import on_command, CommandSession
from plugins.permission import permission
import time  
import subprocess

def cmd(c, timeout=3):
    c = c.split(' ')
    try:
        p = subprocess.run(c, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=timeout)
        return p.stdout.decode()
    except subprocess.TimeoutExpired as e:
        return e.output.decode() + '\nTimeout'
    except Exception as e:
        print(e)
        return 'Fail'

@on_command('status', only_to_me=False)
@permission('ADMIN')
async def status(session: CommandSession):
    res = 'Fail.'
    try:
        res = cmd(session.state['cmd']).strip()
    except Exception as e:
        pass
    await session.send(res)

@status.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['cmd'] = stripped_arg
    else:
        session.state['cmd'] = 'uptime -p'

from buu.session import s

cmds = ['help', 'update', 'check', 'dump']

@on_command('cookies', only_to_me=False)
@permission('ROOT')
async def cookies(session: CommandSession):
    res = '/cookies ' + '|'.join(cmds)
    cmd = session.state['cmd']
    args = session.state['args']
    if cmd == 'check':
        res = '/cookies check'
        if len(args) == 0:
            res = 'Alive' if s.test() else 'Down'
    if cmd == 'update':
        res = '/cookies update {cookies}'
        if len(args) == 1:
            res = 'Success' if s.test(args[0]) else 'Fail'
    if cmd == 'dump':
        res = '/cookies dump'
        if len(args) == 0:
            res = s.cookies.get('session')
    await session.send(res)

@cookies.args_parser
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