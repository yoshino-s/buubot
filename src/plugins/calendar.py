from nonebot import on_command, CommandSession
import requests

@on_command('calendar', only_to_me=False)
async def aff(session: CommandSession):
    await session.send(requests.get('https://api.yoshino-s.online/calendar/google.ics').text)