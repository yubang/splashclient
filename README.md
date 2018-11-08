# splashclient
*简单的splash客户端*

### 安装

```
pip install splashclient
```

### 快速入门

* 初始化客户端，配置代理可以传递{"protocol": "http", "ip": "IP地址", "port": 端口}到参数default_proxy

```
splash_url = "你的splash服务端地址，例如：http://IP:8050"
client = SplashClient(splash_url, default_proxy=None, default_wait=0.1, default_time=30, default_header={
    "User-Agent": "abc"
})
```

* 获取一个渲染后的网页html

```
html = client.render("http://blog.yubangweb.com")
print(html)
```

* 获取页面截图
```
client.png("http://blog.yubangweb.com")
with open("1.png", "wb") as fp:
    fp.write(data)
```