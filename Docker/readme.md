### 使用说明

ytest 基础镜像打包

#### 构建:

docker build --no-cache --build-arg GITHUB_TOKEN=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 --push -t docker-prod-registry.cn-hangzhou.cr.aliyuncs.com/global/fast/ytest-base -f Dockerfile .

### 验证

docker run --rm -it --entrypoint /bin/sh <your_image_name>
