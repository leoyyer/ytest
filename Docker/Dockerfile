FROM python:3.9-alpine

# 安装系统依赖，包括 Java (openjdk11)，并在使用 unzip 时安装它
RUN apk add --no-cache tzdata git wget openjdk11-jre lsof && \
    apk add --no-cache --virtual .build-deps unzip build-base && \
    python3 -m pip install --upgrade pip setuptools wheel && \
    wget https://github.com/allure-framework/allure2/releases/download/2.19.0/allure-2.19.0.zip && \
    unzip allure-2.19.0.zip && \
    mv allure-2.19.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/bin/allure && \
    rm allure-2.19.0.zip && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

# 设置时区为上海时间
ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime

# 设置 JAVA_HOME 环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH="$JAVA_HOME/bin:$PATH"

# 使用 GitHub Personal Access Token 进行认证安装私有仓库
ARG GITHUB_TOKEN
RUN pip install git+https://${GITHUB_TOKEN}:x-oauth-basic@github.com/leoyyer/ytest.git \
    --index-url https://mirrors.aliyun.com/pypi/simple \
    --no-build-isolation  # 禁用隔离环境，确保可以找到全局安装的构建工具

# 暴露端口以便访问 Allure 报告
EXPOSE 8080

# 设置为基础镜像，不需要 entrypoint.sh
CMD ["python3"]
