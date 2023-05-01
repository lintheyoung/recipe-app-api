# 使用Python 3.9和Alpine 3.13作为基础镜像
FROM python:3.9-alpine3.13

# 设置维护者信息
LABEL maintainer="dedemaker.com"

# 设置环境变量，让Python不缓冲输出
ENV PYTHONUNBUFFERED 1

# 复制项目的requirements.txt文件到容器的临时目录
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# 复制app文件夹到容器
COPY ./app /app

# 设置工作目录为/app
WORKDIR /app

# 暴露8000端口
EXPOSE 8000

# 下面的命令将执行以下操作：
# 1. 创建一个名为/py的虚拟环境
# 2. 升级pip
# 3. 安装/tmp/requirements.txt中列出的依赖
# 4. 删除/tmp文件夹
# 5. 创建一个没有密码且无家目录的用户（django-user）
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# 将虚拟环境的二进制文件夹添加到PATH环境变量中
ENV PATH="/py/bin:$PATH"

# 将用户设置为django-user
USER django-user
