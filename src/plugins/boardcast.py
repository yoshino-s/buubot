from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError

from buu.aff import get_aff_list
from buu.user import User

@nonebot.scheduler.scheduled_job('cron', hour=23)
async def boardcast():
    bot = nonebot.get_bot()
    try:
        users = list(map(lambda x: User(*x), get_aff_list()))
        users.sort(key=lambda x:x.data['total'], reverse=True)
        await bot.send_group_msg(group_id=1078525054,
                                 message='\n'.join([user.description() for user in users[0:5]]))
        print('boardcast')
    except CQHttpError:
        pass