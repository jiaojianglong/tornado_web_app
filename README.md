####构建web服务
构建 docker image
tornado_web_app:
docker build -t tornado_web_app:1.5.1 -f dockerfile ./app
启动
docker run -itd --name tornado_web_app -p 8887:8887 tornado_web_app:1.5.1 -e SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:123456@192.168.1.8:3306/tornado_web

数据库构建
alembic init alembic
alembic revision --autogenerate -m "create_user_table"
alembic upgrade head

查看记录和历史
alembic history

回退上一个升级的版本
alembic downgrade -1

