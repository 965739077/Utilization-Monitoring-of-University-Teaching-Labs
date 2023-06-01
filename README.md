# 高校教学实验室利用情况动态可视化大屏

# __软件环境__

Python	3.8

Mysql	8.0

Pycharm	2021


# 依赖安装
安装所需项目所需依赖包，在终端页面输入以下命令即可导入依赖。

`pip install -r requirements.txt`

# 数据库创建

```sql
CREATE DATABASE IF NOT EXISTS laboratory
    DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
```

# 爬虫运行
注意，此爬虫程序以河南工学院教务系统网站为例，如需修改请具备一定的爬虫知识，一切以学习为主，不要违反国家法律法规！

第一步，修改run.py文件中的数据库密码

第二步，修改uplate.py中的数据库密码

运行顺序是run.py --> uplate.py

# 补充说明

数据库用户表SQL语句如下：

```sql
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
)
```
请根据需要进行相应的修改和配置，如有疑问，请参考相关文档或联系开发者。
