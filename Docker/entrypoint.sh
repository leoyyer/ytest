#!/bin/sh

# 日志文件路径（如果你没有 root 权限，使用 /tmp 目录）
LOG_FILE="/var/log/cron.log"

# 如果无法写入 /var/log，回退到 /tmp/cron.log
if ! touch $LOG_FILE 2>/dev/null; then
    LOG_FILE="/tmp/cron.log"
fi

# 捕获 SIGTERM 信号，优雅退出
trap 'echo "⏹️ Script terminated at $(date)" >> $LOG_FILE; exit 0' TERM INT

while true; do
    # 获取当前时间（小时和分钟）并转为四位的 "HHMM"
    current_time=$(date +%H%M)
    
    # 目标时间 "0900" 表示早上 09:00
    target_time="0900"
    
    # 计算当前时间与 09:00 的差距
    if [ "$current_time" -gt "$target_time" ]; then
        # 如果当前时间大于 09:00，计算到明天 09:00 的秒数
        sleep_seconds=$(( (24 * 3600) - $(date +%s) % (24 * 3600) + 32400 )) # 32400 = 9 * 3600
    else
        # 如果当前时间小于 09:00，计算到今天 09:00 的秒数
        sleep_seconds=$(( $(date -d "09:00" +%s) - $(date +%s) ))
    fi

    # 记录日志，显示 sleep 信息
    echo "⏲️ Sleeping for $sleep_seconds seconds until 09:00, current time: $(date)" >> $LOG_FILE
    
    # 睡眠到目标时间
    sleep $sleep_seconds

    # 记录日志，表明脚本开始运行
    echo "🚀 Running script at $(date)" >> $LOG_FILE

    # 切换到 app 目录
    cd /app || {
        echo "❌ Failed to change directory to /app at $(date)" >> $LOG_FILE
        continue  # 如果目录切换失败，跳过本次运行
    }

    # 运行 ytest 并记录日志
    ytest run -p fast -t suite --env test --process True >> $LOG_FILE 2>&1

    # 检查 ytest 运行是否成功
    if [ $? -eq 0 ]; then
        echo "✅ ytest run completed successfully at $(date)" >> $LOG_FILE
    else
        echo "❌ ytest run failed at $(date)" >> $LOG_FILE
    fi
done
