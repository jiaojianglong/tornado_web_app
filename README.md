####构建web服务
构建 docker image
tornado_web_app:
docker build -t tornado_web_app:1.0 -f dockerfile ./app
启动
docker run -itd --name tornado_web_app -p 8887:8887 tornado_web_app:1.0