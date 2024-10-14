#!/bin/bash

while true; do
    # 获取当前时间
    now=$(date +%s)
    
    # 获取今天早上9点的时间戳
    target=$(date -d "09:00" +%s)
    
    # 如果已经过了今天的09点00，计算到明天09点00的时间
    if [ $now -gt $target ]; then
        target=$(date -d "tomorrow 09:00" +%s)
    fi
    
    # 计算当前时间到目标时间的差值（即需要sleep的秒数）
    sleep_seconds=$((target - now))
    
    # 睡眠直到09点
    sleep $sleep_seconds
    
    # 运行脚本并记录日志
    echo "Running script at $(date)" >> /var/log/cron.log
    ytest run -p fast -t suite  --env test --process True >> /var/log/cron.log 2>&1
done
