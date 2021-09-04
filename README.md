# Nginx log helper--可视化Nginx Log数据面板

## 介绍

* 这是一个nginx的log读取程序，由**python3**进行数据处理生成json文件，用户访问时，读取json文件，由**JavaScript**读取python3生成的**json**数据，以图形化的方式，直观地把网站地访问数据显示给用户，用户可以直接对信息进行获取和分析。
* 网页为**静态网页**，**无请求处理程序**，更加安全，只需要定时生成json数据即可使用，不需要处理后端请求
* 设计这个面板的目的是为了了解我的网站的请求情况，我的网站是静态的，无后端程序
* 不建议存在后端程序（如PHP）的网站使用本项目（为了防止攻击信息直接出现导致更严重的攻击）
* nginx/1.16.1 and nginx/1.18.0测试可用



## 运行截图

Demo：https://blog.lxscloud.top/dashboard/index.html



### 数据总览

可以查看**主页访问数**和**请求数**

同时提供**图表**

![1](/img/1.jpg)

### 模块

有五个子模块

![2](/img/2.jpg)

### 模块细分

#### 网站请求次数排名

具有标签功能，信息一目了然

![3](/img/3.jpg)

#### 具备追踪功能

![3](/img/3-1.jpg)

#### 访问者使用最多的浏览器

具有标签功能，标签显示浏览器和异常情况

![4](/img/4.jpg)

#### 同样具备追踪功能

![4-1](/img/4-1.jpg)

#### 访问次数最多的IP

是否显示IP由面板用户决定，请看后部分使用说明

![5](/img/5.jpg)

#### 原始数据

有时候可能有看原始数据的需求

![6](/img/6.jpg)



## 版本

* **V1** 
  * Basic function 
  * 基本功能（访问显示、访问信息）

*  **V1.1** 
   * Repaired sort by date and appended Fetch and Referer showing  
   * 请求量按日期排序、增加“请求”和“来自网址”的显示

* **V2.0**（当前版本）

  * 修复了一个小BUG

  * 优化了代码结构
  
  * 添加 “加载剩余数据” 按钮，在信息比较多的时候不会全部加载到页面
  
  * 访问足迹功能（可以查看访问者还打开了什么网址、什么时候打开的）
  
  * 显示提示标签（数据仅供参考）
  
    

## 使用方法

### 如果只是想尝试

#### 生成json数据

* 打开nginx_log_helper.py

* 修改nginx的log文件的位置（一般为/var/log/nginx/access.log）

  ```python
  test = nginx_read_log("./access.log", "./dashboard/")
  ```

  改为(改成nginx生成access.log的文件的实际位置)

  ```python
  test = nginx_read_log("/var/log/nginx/access.log", "./dashboard/")
  ```

* 修改配置

  默认设置如下

  ```python
  test.gene_json(0, file_n = "data.json")
  test.gene_json(0, file_n = "index_data.json", sort=["/static/img_ness/beian/beian"])
  ```

  可以设置开启IP显示,只要把0改成1(**index_data.json**和**data.json**的文件名一般不需要修改)

  ```python
  test.gene_json(1, file_n = "data.json")
  test.gene_json(1, file_n = "index_data.json", sort=["/static/img_ness/beian/beian"])
  ```

  sort和sort_not参数是用于设置条件， sort用于设置要求出现的URL，sort_no用于排除某个URL，这两个变量的数据类型为list（是**[ ]**）

  * 当sort_not被设置时，生成的JSON中就不会包含设置的URL

  * 当sort被设置时，生成的JSON中就只包含设置的URL

* 详细说明

sort中的”/static/img_ness/beian/beian.jpg“请改成你的主页一定会被请求到的一个文件，以计算主页的访问量

```
sort=["/static/img_ness/beian/beian.jpg"]
```


用于设置生成目录，"./dashboard/"意思是在当前文件夹下的dashboard文件夹里生成json，dashboard目录为网页的目录，请根据实际情况修改
```
./dashboard/
```

  配置修改完就可以开始生成json

  ```bash
  python3 nginx_log_helper.py
  ```

  如果缺少权限，则需要

```bash
sudo python3 nginx_log_helper.py
```

如果access.log的位置没有错误，将会在dashboard文件夹里出现data.json、index_data.json、update_date.json三个新文件

![7](/img/7.jpg)

* nginx_log_helper.py为测试时使用，实际使用请使用run.py



#### 试用

start_server.py提供本地测试的web服务

需要flask包,如果没有安装flask，在debian或者ubuntu使用pip安装flask的方法如下：

```
pip3 install flask
```

注意：仅为尝试的时候才运行，实际环境请不要运行
会开启一个web服务器，端口5000，浏览器打开 http://127.0.0.1:5000/ 即可看到效果

  ```bash
  python3 start_server.py
  ```

**为了安全**，start_server.py最好只是在测试的时候用


### 如果需要部署到网站

#### 要求

* WEB服务器为Nginx

* Python版本为Python3.5或以上



如果没有安装python3，在debian或者ubuntu安装python3的方法如下：

```
sudo apt-get install python3 python3-pip
```



#### 建议&&使用方法

将templates文件夹放在你的web服务器（nginx）的网页目录

* 记得修改run.py的配置，改成你期望的样子

* 配置文件修改一下，使生成的json放到web服务器（nginx）的网页目录的templates文件夹

可以在**改完配置文件**后运行（放在后台运行）

```
nohup python3 run.py &
```

每30分钟会更新一次json数据，时间可以更改run.py的sleep变量

```
sleep = 30 #分钟
```

然后只要访问**你的网站的网址/dashboard/index.html**或**你的网站的网址/dashboard/**就能查看面板



**（建议使用计划任务来运行nginx_log_helper.py, 比运行run.py更可靠）**

# 关于

欢迎访问我的博客：https://blog.lxscloud.top/2021/07/21/Nginx%20log%20helper--%E5%8F%AF%E8%A7%86%E5%8C%96Nginx%20Log%E6%95%B0%E6%8D%AE%E9%9D%A2%E6%9D%BF/

~~下次更新应该会加显示IP归属地（由使用者决定是否打开，此功能需要网络，而且数据生成比较慢）、时区转换~~