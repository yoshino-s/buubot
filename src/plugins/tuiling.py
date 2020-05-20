import json
from typing import Optional

import aiohttp
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression

EXPR_DONT_UNDERSTAND = (
    '听不懂，给👴爬。'
)


@on_command('c', only_to_me=False)
async def tuling(session: CommandSession):
    message = session.state.get('message') or session.current_arg_text.strip()
    print(message)
    reply = await call_tuling_api(session, message)
    if reply:
        await session.send(escape(reply))
    else:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))


@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})


async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': session.bot.config.TULING_API_KEY,
            'userId': context_id(session.ctx, use_hash=True)
        }
    }

    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError) as e:
        print(e)
        return None