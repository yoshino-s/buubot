from datetime import datetime

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

from buu.aff import get_aff_list
from buu.user import User

print(nonebot.scheduler)

@nonebot.scheduler.scheduled_job('cron', minute='*/10')
async def update():
    bot = nonebot.get_bot()
    try:
        print('Updating')
        users = list(map(lambda x: User(*x), get_aff_list()))
        await bot.send_private_msg(user_id=1735439536,
                                 message=f'刚刚更新了数据，好开心')
        print('Updated')
    except CQHttpError:
        pass
