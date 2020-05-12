from nonebot import on_command, CommandSession

@on_command('help', only_to_me=False)
async def aff(session: CommandSession):
    await session.send("""/aff [aff1,aff2...]
/rank {num}|[id:]{id1,id2,...}""")