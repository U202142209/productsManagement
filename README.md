# 说明文档

这是一个半成品

## 1. 连接服务器

```text
服务器IP地址:ip
用户名:user
密码:password
```

## 2. 项目部署命令

### 2.1 运行代码

虚拟环境配置

```text
# 查看当前系统中已存在的虚拟环境
conda info --envs

# 创建一个名为kydbenv的Python虚拟环境，并指定Python版本为3.8.10：
conda create --name kydbenv python=3.8.10

# 使用以下命令激活虚拟环境
conda activate kydbenv   # 在 Windows 上：
source activate kydbenv  # 在 macOS/Linux 上：

# 添加清华大学镜像源：
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

# 激活虚拟环境后，可以使用以下命令安装所需的模块，例如：
conda install django==4.2.8
conda install pandas==2.0.3 
conda install openpyxl==3.0.10
conda install requests==2.31.0
pip install django-simple-captcha==0.6.0  # conda没找到
pip install django-cors-headers==4.3.1    # conda没找到
pip install django-ckeditor==6.7.0        # conda没找到
conda install pyjwt==2.4.0
conda install py7zr==0.20.5
pip install pillow==10.1.0
pip install pymysql==0.9.3

# 退出虚拟环境
## 在 Windows 上
conda deactivate
## 在 macOS/Linux 上：
source deactivate
```

测试启动项目

```text
进入项目路径
cd /var/opt/productsManagement

# 迁移数据库
python3 manage.py makemigrations
python3 manage.py migrate

# 创建缓存表
python3 manage.py createcachetable

# 创建超级管理员
python3 manage.py createsuperuser

# 收集静态文件
python3 manage.py collectstatic

# 运行代码
python3 manage.py runserver
```

ubuntu后台运行程序

```text
参考连接：
https://www.jianshu.com/p/09d86aad9fa4?u_atoken=de1189fb-e44f-407a-8c7e-ff3d08b6edb3&u_asession=01Zw2Qv526FNuXFRlY2QcKlg-Cpq_-bKLiElcEagdf4GVku-Kp4PvVjjK-P9NADOiuX0KNBwm7Lovlpxjd_P_q4JsKWYrT3W_NKPr8w6oU7K9wHnb2mCdMACSGri__bMH13KmjkU3JT7ddtoHBlecZWGBkFo3NE
# 创建窗口
screen -S name
# 启动django
python3 manage.py runserver 0.0.0.0:8888
# ctrl-a d 先按ctrl+a，再按d，dettach，此时你可以关闭连接了，做自己想做的事情去。
# 查看当前有哪些会话，并显示id
screen -ls 
# 恢复会话
screen -r <id> 
# 删除会话
screen -S <id> -X quit 

```

### 2.2 nginx

```text
nginx配置文件路径:
cd /etc/nginx/conf.d
# 启动nginx
sudo systemctl start nginx
sudo service nginx start
# 重启nginx
sudo systemctl  reload nginx
# 停止nginx
sudo service nginx stop
```

nginx文件配置内容

```text
nginx配置文件路径:
cd /etc/nginx/conf.d

# 删除配置文件
rm -rf app.conf

# 编辑配置文件
sudo vim app.conf
# 文件内容
server {
    listen 80;
    server_name anyue.online;

    location / { 
        proxy_pass http://127.0.0.1:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 如果需要将 CSRF 令牌也转发，可以添加如下设置
        proxy_set_header X-XSRF-TOKEN $http_x_xsrf_token;
    }
    
    location /static { 
        alias /var/opt/productsManagement/static;
    }	        
}

```