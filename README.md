# serv00-keep-on
serv00/ct8平台  **灵活** 保活文件 

serv00/ct8 platform **flexible** keep-ON file. 

# start
在serv00/ct8的panel内删除域名，重新添加
添加时
**

Website type = python

Python binary = python3.11

**

然后

`git clone https://github.com/sakura747/serv00-keep-on.git`

### 第二步
在public_python下
创建 start.sh，
内容自定义
例子：
```shell
#!/bin/bash

# 创建一个名为“sakura”文件
touch sakura

echo "文件 'sakura' 已创建"
```
先在ssh运行./start.sh，测试运行成功再来
如果运行不报错，即可进入下一步
## 第三步
再创建一个passenger_wsgi.py
内容为
```shell
import sys, os
sys.path.append(os.getcwd())

os.environ['runMaster'] ="./start.sh"

from application import app as application
```
这里的start.sh值上面的start.sh文件
然后在panel—— Manage ——restat


最后访问你的域名/start-local-file即可保活

#完结

# 什么不能用？肯定啊，不然为什么叫 **灵活保活**


# 闲杂问题不回，自行摸索
