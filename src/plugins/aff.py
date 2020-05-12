from nonebot import on_command, CommandSession
from buu.aff import get_aff_list


@on_command('aff', only_to_me=False)
async def aff(session: CommandSession):
    affs = session.state['affs']
    print(affs)
    s = f'在{",".join(session.state["affs"])}中有：'
    l = []
    for a in affs:
        l += [i[1] for i in get_aff_list(a)]
    s+=', '.join(l)
    print(s)
    await session.send(s)

@aff.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.state['affs'] = stripped_arg.split(',')
    else:
        session.state['affs'] = ['V&N', '/r']