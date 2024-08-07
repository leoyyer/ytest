备用仓库
https://github.com/pengdaan/ytest.git

查看备用仓库分支
git fetch backup

推送代码到备用仓库
git push backup backup/main

创建备份库的分支:
git checkout -b backup-main backup/main

添加/推送
git add .
git commit "xxxx"
git push backup main:main

切换:
git checkout backup-main
