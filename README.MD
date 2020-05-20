# Readme

## What is this?

A bot based on coolq, served as a qq bot for buuoj data searcher.

---

## How to use?

Search docs by yourself.

[cqhttp](https://cqhttp.cc/)  
[nonebot](https://nonebot.cqp.moe/)  
[docker-compose](https://docs.docker.com/compose/)

---

## Simple way to use

### Config

Change the `VNC_PASSWD: "password"` in the `docker-compose.yml`, to protect your vnc connect, or only bind port to the localhost.

### Start

```sh
# sudo
docker-compose build
docker-compose up -d
```

And connect to the `localhost:9000` to configure the coolq.

> Hint: Some qq account cannot use as the bot. Try to use some much older account.

### Log

```sh
docker-compose logs -f
```

---

## Warning

This is not a official bot, and the API used is also built by myself, also not fficial. I don't own the data.  

Secondary development is allowed. but **Do not use this for commercial purposes.**

---

## Thanks

[Glzjin](https://www.zhaoj.in/) Thanks for Glzjin's API.  
[ERROR404](https://www.lhyerror404.cn/) Thanks for debugging with me.
