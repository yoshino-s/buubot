from python:3.6

COPY ./src /app

WORKDIR /app

RUN pip install nonebot python-dateutil bs4 requests pytz -i https://mirrors.aliyun.com/pypi/simple \
 && pip install "nonebot[scheduler]"  -i https://mirrors.aliyun.com/pypi/simple \
 && echo 'flag{B0t_als0_ha5_a_f1aG}' > /flag

CMD ["python3", "bot.py"]