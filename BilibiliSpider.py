# -*- coding: utf-8 -*-

import requests
from requests.packages import urllib3
import re
import ast
import os
import subprocess

urllib3.disable_warnings()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'Connection': 'close'
}


class BilibiliSpider:

    def __init__(self, url):
        self.flag = None
        self.URL = url
        self.title = ""

        # 获取服务器响应
        self.response = self.getResponse()
        # print(self.response)


    """
    获取服务器响应
    """

    def getResponse(self):
        headers['referer'] = self.URL  # 注意: referer和user-agent是必须要加的
        res = requests.get(self.URL, headers=headers, verify=False)
        try:
            res.raise_for_status()
            res = res.text
            self.title = re.search('<title data-vue-meta="true">.*?</title>', res).group(0)[28:-22].replace(' ', '_')
            self.title = self.title.replace('/', "or").replace('\\', "or").replace('《', "").replace('》', "")
            return res
        except requests.exceptions.HTTPError as err:
            return str(err)

    """
    获取文本信息
    """

    def getText(self):
        # 时间
        time = re.search('<div class="pubdate-ip-text" data-v-aed3e268>.*?</div>', self.response).group(0)[45:-6]
        # 描述
        pattern = re.compile('<meta data-vue-meta="true" itemprop="description" name="description" content=.*?>',
                             re.DOTALL)  # 匹配换行符
        description = pattern.search(self.response).group(0)[78:].replace('\n', '戆')  # 将换行符替代为标志词
        for index, value in enumerate(description):  # 去掉标志词后的广告
            if value == '戆':
                description = description[:index]
                break
        # 作者 + 时间
        text1 = re.search("视频作者.*?作者简介", description).group(0)[:-6].replace(' ', ':').replace('、',
                                                                                                      '  ') + "  " + time
        # 描述
        text2 = re.search("视频播放量.*?视频作者", description).group(0)[:-6].replace(' ', ':').replace('、', '  ')
        # 简介
        pattern = re.compile('span class="desc-info-text".*?<', re.DOTALL)
        text3 = re.search(pattern, self.response).group(0)[44:-1]
        return text1[2:] + "\n" + text2[2:] + "\n\n简介：\n" + text3

    """
    打印音频/音频信息
    """

    def show_param(self, downloadDic, flag):
        str = (f"id:{downloadDic['id']}\nbandwidth:{downloadDic['bandwidth']}\nmimeType:{downloadDic['mimeType']}\n"
               f"codecs:{downloadDic['codecs']}\n")
        if flag == 0:
            str += f"width:{downloadDic['width']}\nheight:{downloadDic['height']}\nframeRate:{downloadDic['frameRate']}\n"
        str += f"backupUrl:{downloadDic['backupUrl'][0]}\n"
        return str

    """
    下载文档
    """

    def downloadText(self):
        path = "..\\res\\" + self.title + ".txt"
        print("保存路径:", path)
        with open(path, "w", encoding='utf8') as f:
            f.writelines([self.title, self.t1, self.t2, self.t3])
            f.close()

    """
    下载图片
    """

    def downloadImage(self):
        # 获取图片
        downloadURL = "https:" + re.search('itemprop="image".*?>', self.response).group(0)[26:-2]
        for index, value in enumerate(downloadURL):
            if value == '@':
                downloadURL = downloadURL[:index]
        path = "..\\res\\" + self.title + downloadURL[-4:]
        print("保存路径:", path)
        with open(path, "wb") as f:
            f.write(requests.get(downloadURL, headers=headers).content)
            f.close()

    """
    下载音频\视频
    """

    def downloadAudio(self, flag=0):
        # 获取json格式的下载信息
        pattern = ""
        if flag == 0:  # 音频
            pattern = '"audio":.*?"dolby"'
        if flag == 1:  # 视频
            pattern = '"video":.*?"audio"'
        jsonList = re.search(pattern, self.response)[0][9:-9].split('},{')  # 获取由字符串类型为元素所组成的列表
        print(jsonList)
        # 将列表中的元素字符串类型转换成字典类型
        for i in range(len(jsonList)):
            # 拼接为正常的字符串字典
            if jsonList[i][-1] != '}':
                jsonList[i] += '}'
            if jsonList[i][0] != '{':
                jsonList[i] = '{' + jsonList[i]
            # 字符串转列表
            jsonList[i] = ast.literal_eval(jsonList[i])

        # 获取下载url
        downloadURL = ""
        for dic in jsonList:  # 下载列表存放以字典为元素的列表
            if flag == 0:
                downloadURL = dic['backupUrl'][0]
                print(self.show_param(dic, flag))  # 打印信息
                break
            if flag == 1 and dic['codecs'][0] == 'h':  # 视频codecs选择hev
                downloadURL = dic['backupUrl'][0]
                print(self.show_param(dic, flag))  # 打印信息
                break

        # 保存下载的音频/视频
        path = "..\\res\\" + self.title
        if flag == 0:
            path += "_audio.mp4"
        if flag == 1:
            path += "_temp.mp4"
        print("保存路径:", path)
        with open(path, "wb") as f:
            f.write(requests.get(downloadURL, headers=headers).content)
            f.close()

    """
    下载视频
    这里是使用ffmpeg合成音频视频
    """

    def downloadVideo(self):
        if self.title + "_audio.mp4" not in os.listdir('../res'):
            self.downloadAudio()
        self.downloadAudio(flag=1)
        audio = "..\\res\\" + self.title + "_audio.mp4"
        temp = "..\\res\\" + self.title + "_temp.mp4"
        video = audio[:-10] + '_video.mp4'
        cmd = f'.\\lib\\ffmpeg.exe -i {audio} -i {temp} -acodec copy -vcodec copy {video}'  # 这里是调用ffmpeg  # D:\Pycharm\ffmpeg\bin\
        subprocess.call(cmd, shell=True)  # 调用ffmpeg合并音频和视频
        os.remove(temp)
        os.remove(audio)


if "__main__" == __name__:
    url = r"https://www.bilibili.com/video/BV1UM4y1G77m/?spm_id_from=333.999.0.0&vd_source=0dbce90849757bb29232a98ebbb71efb"  # BV1qm421s7MR
    bilibiliSpider = BilibiliSpider(url)
    # bilibiliSpider.downloadImage()
    # bilibiliSpider.downloadAudio()
    # bilibiliSpider.downloadVideo()
