from threading import Thread
import pymysql
import requests
from bs4 import BeautifulSoup
import time


class MyThread(Thread):
    def __init__(self, spider1, args):
        '''
        :param func: 可调用的对象
        :param args: 可调用对象的参数
        '''
        Thread.__init__(self)   # 不要忘记调用Thread的初始化方法
        self.func = spider1
        self.args = args

    def run(self):
        self.func(*self.args)

def insert_mysql(data):
    db = pymysql.connect("localhost", "root", '', "test")
    cursor = db.cursor()
    cursor.execute("insert into thread_test value(%s,%s)", data)
    db.commit()
    cursor.close()
    db.close()

def spider(page):
    url = 'http://quotes.toscrape.com/page/{}/'.format(page)
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    quotes = soup.select('div.quote')
    # print(len(quotes))
    for quote in quotes:
        text = quote.find_all('span')[0].text
        author = quote.select('small.author')[0].text
        print('text', text)
        print('author', author)
        print('**************', '\n')
        data = (text, author)
        insert_mysql(data)


def main():
    # 创建 Thread 实例
    t1 = MyThread(spider, (1,))
    t2 = MyThread(spider, (2,))
    t3 = MyThread(spider, (3,))
    # 启动线程运行
    t1.start()
    t2.start()
    t3.start()
    # 等待所有线程执行完毕
    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print('3个线程爬取需要{}S'.format(end-start))