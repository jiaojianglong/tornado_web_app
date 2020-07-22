FROM python:3.6

COPY ./requirements /usr/local/bin/tornado_web_app/requirements
WORKDIR /usr/local/bin/tornado_web_app/
RUN pip install -r requirements -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./ /usr/local/bin/tornado_web_app
ENV PYTHONPATH "${PYTONPATH}:/usr/local/bin/tornado_web_app"

CMD ["python", "/usr/local/bin/tornado_web_app/app/start.py", "--port=8887", "--apps=auth"]