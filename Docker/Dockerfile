FROM python:3.9-slim

# 安装系统依赖，包括 Java、wget 和 unzip
RUN apt-get update && \
    apt-get install -y tzdata git wget unzip default-jdk lsof && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 设置时区为上海时间
ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# 设置 JAVA_HOME 环境变量
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="$JAVA_HOME/bin:$PATH"

# 创建工作目录
WORKDIR /app

# 安装 Allure CLI
RUN wget https://github.com/allure-framework/allure2/releases/download/2.19.0/allure-2.19.0.zip && \
    unzip allure-2.19.0.zip && \
    mv allure-2.19.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/bin/allure && \
    rm allure-2.19.0.zip

# 使用 GitHub Personal Access Token 进行认证安装私有仓库
ARG GITHUB_TOKEN  # 添加构建参数
RUN pip uninstall -y ytest
RUN pip install git+https://${GITHUB_TOKEN}:x-oauth-basic@github.com/leoyyer/ytest.git

# 暴露端口以便访问 Allure 报告
EXPOSE 8080

# 设置为基础镜像，不需要 entrypoint.sh
CMD ["python3"]
