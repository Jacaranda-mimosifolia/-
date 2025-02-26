# bilibili爬虫


## 实现以下功能:

- 视频封面爬取
- 音频爬取
- 视频爬取


## 文件结构:

- MainWindow.py--------------------------------------------程序主界面
- SearchWidget.py------------------------------------------搜索界面
- downloadWidget.py---------------------------------------下载界面
- BilibiliSpider.py---------------------------------------------爬虫代码



## 运行项目

1. 安装依赖包

   `pip install -r requirements.txt`

   需要注意的是PyQt5与sip必须是对应的版本

   最简单的就是将两者都更新到最新版本

   `pip install -U PyQt5`

   `pip install -U sip`

2. 运行`MainWindow.py`启动项目
3. 下载路径,位于更目录下的res/文件夹中

## 打包项目

1. 生成可执行`exe`文件

   `pyinstaller -F -w --clean --icon=./images/MainWindow_1.ico MainWindow.py`

2. 生成的文件位于项目文件夹`dist`下,此为自动生成文件夹。

## 项目缺点
1. 对视频名称处理不完备,可能会因为视频名称导致保存路径无效而出错误
2. 根据收藏夹网址遍历爬取功能,有待开发
3. 未添加登录bilibili功能,所爬取到的音频及视频质量有限
4. 用户选择存放路径功能有待开发
5. 操作日志功能有待开发
