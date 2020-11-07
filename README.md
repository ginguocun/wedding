
[TOC]

## 1. 项目介绍

### 1.1. 介绍

项目后端基于 Django 3.1 进行开发。服务采用 Nginx 代理静态文件，可以参考 nginx.conf 进行配置，Django 服务使用 uwsgi 进行启动，基于 wedding_uwsgi.ini 配置文件。

项目目录

```

```



### 1.2. 项目依赖
- Nginx
- python 3.6-3.8

## 2. 服务安装与升级

### 2.1. 服务安装

#### 2.1.1. 拉取代码

进入 /opt 目录拉取代码

```shell
git clone https://github.com/ginguocun/wedding.git
```

#### 2.1.2. 进入指定的路径

```sh
cd /opt/wedding
```

#### 2.1.3. 启动虚拟环境

```sh
python3 -m venv venv
source venv/bin/activate
```

#### 2.1.4. 更新 setuptools pip

```sh
pip3 install --upgrade setuptools pip
```

#### 2.1.5. 安装依赖

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2.1.6. 配置 settings 文件

在 wedding/wedding 目录下面添加配置文件 settings.py，并且根据里面的  todo 更新配置

```python


```

#### 2.1.7. 迁移数据库 

```sh
python3 manage.py migrate
```

#### 2.1.8. 创建超级用户

```sh
python3 manage.py createsuperuser
```

运行以上命令，输入用户名和密码

#### 2.1.9. 项目启动

测试服务启动

```sh
python3 manage.py runserver 0.0.0.0:80
```

在浏览器的地址输入框输入ip，然后后面添加 /admin/ ，看能否跳转到登录页面，如果跳转成功说明服务已经正常启动了。但是用户直接访问 Django 服务的部署方式不适合生产环境。

### 2.2. 服务部署

服务采用Nginx+uwsgi+Django 的方式进行部署。

```
the web client <-> Nginx <-> the socket <-> uwsgi <-> Django
```

可以参照https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html

#### 2.2.1. 安装和配置 Nginx

下载和安装 Nginx

```sh
apt-get install -y nano nginx
```

拷贝配置文件

```sh
cp /opt/wedding/nginx.conf /etc/nginx/sites-available/default
```

用 nano 编辑器打开Nginx 的配置文件 default

```sh
nano /etc/nginx/sites-available/default
```

将文件里面的 server_name 改为自己的网址，然后运行以下代码测试配置是否正常。

```sh
nginx -t
```

如果输出如下，说明配置已经成功。否则可能有问题。

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

启动 nginx 服务，可以运行以下命令。

```sh
/etc/init.d/nginx start
```

如果启动失败，可能是由于 80 端口被占用，需要先关闭相关的服务。

如果服务已经启动，配置文件更新了，可以运行以下命令重新加载配置，使配置生效。

```sh
nginx -s reload
```

服务正常启动以后访问 ip 可以看到 **Welcome to nginx!** 字样。

### 2.2.2. 启动 uwsgi

可以使用 wedding_uwsgi.ini 进行项目启动，运行以下代码

```
cd /opt/wedding  && source venv/bin/activate
uwsgi --ini /opt/wedding/wedding_uwsgi.ini
```

### 2.3. 服务升级

服务升级需要的命令

```sh
cd /opt/wedding  && source venv/bin/activate
git pull
python3 manage.py migrate
ps auxw | grep wedding_uwsgi
uwsgi --reload /opt/wedding/uwsgi/uwsgi.pid
ps auxw | grep wedding_uwsgi
```

#### 2.3.1. 进入指定的路径

```sh
cd /opt/wedding
```

#### 2.3.2. 启动虚拟环境

```sh
source venv/bin/activate
```

#### 2.3.3. 拉取最新的代码

```sh
git pull
pip install -r requirements.txt
python3 manage.py migrate
```

#### 2.3.4. 重启服务

```sh
ps auxw | grep wedding_uwsgi
uwsgi --reload /opt/wedding/uwsgi/uwsgi.pid
```

服务启动命令

```sh
uwsgi --ini /opt/wedding/wedding_uwsgi.ini
```
