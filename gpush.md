备用仓库
https://github.com/pengdaan/ytest.git

查看备用仓库分支
git fetch backup

1. 推送代码到备用仓库 1.切换:
   git checkout backup-main

2. 添加/推送
   git add .
   git commit "xxxx"
   git push backup backup/main

创建备份库的分支:
git checkout -b backup-main backup/main
