# Nginx log helper--可视化Nginx Log数据面板

## 介绍

* 这是一个nginx的log读取程序，由**python3**进行数据处理生成json文件，用户访问时，读取json文件，由**JavaScript**读取python3生成的**json**数据，以图形化的方式，直观地把网站地访问数据显示给用户，用户可以直接对信息进行获取和分析。
* 网页为**静态网页**，**无请求处理程序**，更加安全，只需要定时生成json数据即可使用，不需要处理后端请求
* 设计这个面板的目的是为了了解我的网站的请求情况，我的网站是静态的，无后端程序
* 不建议存在后端程序（如PHP）的网站使用本项目（为了防止攻击信息直接出现导致更严重的攻击
* nginx/1.16.1 and nginx/1.18.0测试可用

## 运行截图

### 数据总览

可以查看**主页访问数**和**请求数**

同时提供**图表**

![1](/img/1.jpg)

### 模块

有四个子模块

![2](/img/2.jpg)

### 模块细分

#### 网站请求次数排名

![3](/img/3.jpg)

#### 访问者使用最多的浏览器

![4](/img/4.jpg)

#### 访问次数最多的IP

是否显示IP由面板用户决定，请看后部分使用说明

![5](/img/5.jpg)

#### 原始数据

有时候可能有看原始数据的需求

![6](/img/6.jpg)



## 使用方法

### 如果只是想尝试

#### 生成json数据

* 打开nginx_log_helper.py

* 修改nginx的log文件的位置（一般为/var/log/nginx/access.log）

  ```python
  test = nginx_read_log("./access.log", "./templates/")
  ```

  改为(改成nginx生成access.log的文件的实际位置)

  ```python
  test = nginx_read_log("/var/log/nginx/access.log", "./templates/")
  ```

* 修改配置

  默认设置如下

  ```python
  test.gene_json(0, file_n = "data.json")
  test.gene_json(0, file_n = "index_data.json", sort=["/static/img_ness/beian/beian"])
  ```

  可以设置开启IP显示(后面的生成json的文件名不需要修改)

  ```python
  test.gene_json(1, file_n = "data.json")
  test.gene_json(1, file_n = "index_data.json", sort=["/static/img_ness/beian/beian"])
  ```

  sort sort_not参数是用于设置条件

  sort中的”/static/img_ness/beian/beian“请改成你的主页一定会被请求到的一个文件，以计算主页的访问量

  ```
  sort=["/static/img_ness/beian/beian"]
  ```
  
  用于设置生成目录，"./templates/"意思是在当前文件夹下的templates文件夹里生成json
  ```
  ./templates/
  ```

  配置修改完就可以开始生成json

  ```bash
  python3 nginx_log_helper.py
  ```

  如果access.log的位置没有错误，将会在templates文件夹里出现data.json、index_data.json、update_date.json三个新文件

![7](/img/7.jpg)

#### 试用

* 提供本地测试web服务

  注意：仅为尝试的时候才运行，实际环境请不要运行

  会开启一个web服务器，端口5000，浏览器打开http://127.0.0.1:5000/即可看到效果
  
  ```bash
python3 start_server.py
  ```
  

### 部署到网站

* 觉得有需要，可以部署到你的网站

将templates文件夹放在你的web服务器（nginx）的网页目录



* 配置文件修改一下，使生成的json放到web服务器（nginx）的网页目录的templates文件夹

可以在**改完配置文件**后运行（放在后台运行）

```
nohup python3 run.py &
```

每30分钟会更新一次json数据，时间可以更改run.py的sleep变量

```
sleep = 30 #分钟
```



然后只要访问**你的网站/templates/index.html**就能查看面板
