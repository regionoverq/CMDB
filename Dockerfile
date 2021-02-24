
FROM  python:3.8.3
ENV PYTHONUNBUFFERED=1
RUN sed -i "s/deb.debian.org/mirrors.cloud.tencent.com/g" /etc/apt/sources.list
WORKDIR /code
COPY requirements.txt /code/
RUN python -m pip install --upgrade pip -i https://pypi.mirrors.ustc.edu.cn/simple
RUN  pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple
COPY . /code/