from nonebot import on_command, CommandSession
import requests

@on_command('sucker', only_to_me=False)
async def aff(session: CommandSession):
    await session.send(requests.get('https://api.ixiaowai.cn/tgrj/').text)