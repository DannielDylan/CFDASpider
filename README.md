# CFDASpider
使用requests+xpath抓取CFDA的化妆品许可证书
## 运行环境
安装python3 and mysql 数据库

## 下载使用
将项目克隆到本地

```
$ git@github.com:DannielDylan/CFDASpider.git
```

进入到工程目录

``` cd CFDA
```
默认使用mysql数据库，数据库配置默认用户名与密码
user为"root"，password为"123456"
```
DBKWARGS = {
            "host": 'localhost',
            "user": 'root',
            "password": '123456',
            "db": 'CFDA',
            "charset": 'utf8'

        }
```
Mysql：导入数据表结构

+-----------------+------------------+------+-----+---------+----------------+
| Field           | Type             | Null | Key | Default | Extra          |
+-----------------+------------------+------+-----+---------+----------------+
| id              | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| NAME_ID         | varchar(50)      | NO   |     | NULL    |                |
| EPS_NAME        | varchar(50)      | NO   |     | NULL    |                |
| PRODUC_SN       | char(30)         | NO   |     | NULL    |                |
| CITY_CODE       | char(100)        | NO   |     | NULL    |                |
| QF_MANAGER_NAME | varchar(100)     | NO   |     | NULL    |                |
| XK_DATE         | datetime         | NO   |     | NULL    |                |
| XC_DATE         | datetime         | NO   |     | NULL    |                |
+-----------------+------------------+------+-----+---------+----------------+
```
mysql> create database cfda charset utf8;
Query OK, 1 row affected (0.00 sec)
mysql> use cfda
Database changed
mysql> create table CFDA(id int unsigned not null auto_increment primary key,NAME_ID varchar(100) not null,EPS_NAME varchar(50) not null,PRODUCT_SN char(30) not null,CITY_CODE char(10) not null,QF_MANAGER_NAME varchar(100) not null,XK_DATE datetime not null,XC_DATE datetime not null);
Query OK, 0 rows affected (0.34 sec)

```

运行启动脚本 python CFDAspider.py

``` $ python CFDA_DEMO.py
```
