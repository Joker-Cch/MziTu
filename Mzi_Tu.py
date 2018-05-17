#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import time
import random
import requests
from lxml import etree
import gevent
from gevent import monkey
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
monkey.patch_all()


class Spider(object):
    # 初始化
    def __init__(self, t):
        self.base_url = 'http://www.mzitu.com/%s/' % t
        self.headers = {
                        # 'Pragma': 'no-cache',
                        # 'Accept-Encoding': 'gzip, deflate',
                        # 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                        # 'Cache-Control': 'no-cache',
                        # 'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/59.0.3071.115 Safari/537.36',
                        # 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                        'Host': 'i.meizitu.net',
                        'Referer': 'http://www.mzitu.com/',
                    }

    """ # 获取每种类型的总页数
    def get_page(self):
        response = requests.get(self.base_url, self.headers).content
        html = etree.HTML(response)
        return html.xpath('//div[@class="nav-links"]/a[last()-1]/text()')[0]"""

    # 获取每个主页的url列表
    def urls_list(self, x):
        # 分析base_url
        response = requests.get(x, self.headers, timeout=1).content
        time.sleep(1)
        html = etree.HTML(response)
        # 获取 urls 列表并返回

        return html.xpath('//ul[@id="pins"]/li/a/@href')

    # 发起请求
    def send_request(self, url):
        print '发起对 %s 请求' % url
        response = requests.get(url, self.headers, timeout=1).content
        html = etree.HTML(response)
        self.parse_page(url, html)

    # 返回响应、分析页面、提取信息
    def parse_page(self, url, html):

        # 标题
        title = html.xpath('//h2[@class="main-title"]/text()')[0]

        # 总页数
        pages = html.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]

        jpg_list = []

        print '正在获取图片连接列表...'
        for num in range(int(pages)):

            link = '{}/{}'.format(url, num + 1)

            print '正在读取：%s' % link
            try:
                response = requests.get(link, self.headers, timeout=1).content
                html = etree.HTML(response)
            except Exception as e:
                print e
                response = requests.get(link, self.headers, timeout=1).content
                html = etree.HTML(response)

            jpg = html.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            jpg_list.append(jpg)

        print '准备写入...'
        time.sleep(random.randint(1, 3))
        self.write(title, jpg_list)

    # 写入文件
    def write(self, title, jpg_list):

        f_name = "【%sP】%s" % (str(len(jpg_list)), title)
        os.mkdir(f_name)
        print '正在下载...'
        k = 1
        for x in jpg_list:
            file_name = '%s/%s/%s.jpg' % (os.path.abspath('.'), f_name, k)
            try:
                with open(file_name, 'wb') as f:
                    f.write(requests.get(x, headers=self.headers, timeout=1).content)
                    print '已下载：%s' % file_name
            except Exception as e:
                print e
            k += 1
        print '%s 已保存' % f_name

        time.sleep(5)

    # 启动器
    def main(self):
        print '您所爬取的类型为：%s' % tp
        start = int(raw_input('请输入起始页：'))
        end = int(raw_input('请输入末尾页：'))

        # 遍历主地址
        try:
            for num in range(start, end + 1):
                if num:
                    url = self.base_url + 'page/' + str(num) + '/'
                    time.sleep(3)
                    print '正在对 %s 进行爬取...' % url

                    # spawn_list = []
                    for i in self.urls_list(url):
                        # job = gevent.spawn(self.send_request, i)
                        # spawn_list.append(job)
                        # gevent.joinall(spawn_list)
                        self.send_request(i)
                    print '已完成 %s 抓取' % url

                else:
                    print '已执行完毕、感谢使用！'

        except Exception as e:
            print e


if __name__ == '__main__':

    print '【0】：性感\t【1】：日本\t【2】：台湾\t【3】：清纯'
    tp_dict = {'0': 'xinggan',
               '1': 'japan',
               '2': 'taiwan',
               '3': 'mm'}

    tp = tp_dict.get(raw_input('请选择类型：'))

    spider = Spider(tp)
    spider.main()