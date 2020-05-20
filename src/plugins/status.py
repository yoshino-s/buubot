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
