from multiprocessing.managers import BaseManager
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser

class SpiderWork():
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        server_addr = '127.0.0.1'
        print('Connect to server %s'%server_addr)
        self.m = BaseManager(address = (server_addr,8001),authkey = b'baike')
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print('init finish')

    def crawl(self):
        while True:
            try:
                if not self.task.empty():
                    url = self.task.get()
                    if url == 'end':
                        print('控制节点通知爬虫结束工作')
                        self.result.put({'new_urls':'end','data':'end'})
                        return
                    print('爬虫正在解析%s'%url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls,data = self.parser.parser(url,content)
                    self.result.put({'new_urls':new_urls,'data':data})
            except EOFError:
                print('连接工作节点失败')
                return
            except Exception:
                print(Exception)
                print('Crawl fail')

if __name__ == '__main__':
    spider = SpiderWork()
    spider.crawl()