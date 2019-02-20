# _*_ coding:utf-8 _*_
import os
import time
from tkinter import *
from tkinter import messagebox
import json
import mp3play
from urllib import request
import urllib
from threading import Thread
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class music(object):
    def __init__(self):
        # 开启
        self.start = 1
        # 关闭
        self.stop = 0
        self.list_search_id = []
        self.list_search_name = []
        self.list_search_author = []
        self.list_play_id = []
        self.list_play_name = []
        self.list_play_author = []
        self.status = self.stop
        self.display_name = None
        # 保存列表的名字
        self.save_list_txt_name = 'list_play.txt'
        # 当前选择id的序号
        self.current_id = 0
        # 判断id是否改变
        self.change_id = self.stop
        # 歌曲下载路径
        self.save_path = 'C:\\Users\\hasee\\Desktop\\music-player\\music-player\\'
        self.create_list_txt()
        self.build_task()
        self.create_module()
        self.read_list_txt()

    def create_list_txt(self):
        if not os.path.isfile(self.save_list_txt_name):
            with open(self.save_list_txt_name, 'wt', encoding='utf-8') as list_play:
                pass
    def delete_one_list_txt(self,number):
        with open(self.save_list_txt_name, 'rt', encoding='utf-8') as list_play:
            list_source = list_play.readlines()
            list_source.pop(number)
        with open(self.save_list_txt_name, 'wt', encoding='utf-8') as list_play:
            for value in list_source:
                list_play.write(value)

    def read_list_txt(self):
        with open(self.save_list_txt_name, 'rt', encoding='utf-8') as list_play:
            #print('values', list_play.readlines())
            for value in list_play.readlines():
                value = tuple(value.split(' '))
                name,author,ids = value[0],value[1],int(value[2].strip())
                self.list_play_id.append(ids)
                self.list_play_name.append(name)
                self.list_play_author.append(author)
                self.listbox_play.insert(END, self.list_play_name[-1] + "-" + self.list_play_author[-1])
                self.listbox_play_delete.insert(END, '删除')

    def write_one_list_txt(self, name,author,ids):
        with open(self.save_list_txt_name, 'at', encoding='utf-8') as list_play:
            list_play.write(name + ' ' + author + ' ' + str(ids) + '\n')

    def write_all_list_txt(self, name_list, author_list, id_list):
        with open(self.save_list_txt_name, 'wt', encoding='utf-8') as list_play:
            for name, author, ids in (name_list, author_list, id_list):
                list_play.write(name + ' ' + author + ' ' + str(ids) + '\n')

    def build_task(self):
        self.thread = Thread(target=self.task_play)
        self.thread.setDaemon(True)
        self.thread.start()

    def task_play(self):
        while True:
            time.sleep(0.01)
            self.change_id = self.stop
            if self.status == self.start:
                for i in self.list_play_id[self.current_id:]:
                    os.system("taskkill /F /IM ffplay.exe 2>NUL 1>NUL")
                    self.paly_http(i)
                    if self.change_id == self.start:
                        break
                if self.change_id == self.stop:
                    self.current_id = 0

    def music(self):
        self.list_search_id = []
        self.list_search_name = []
        text = self.entry.get()
        text = text.encode('utf-8')
        text = request.quote(text)
        if not text:
            messagebox.showinfo('温馨提示', '您可以输入以下内容进行搜索\n1.歌曲名\n2.歌手名\n3.部分歌词')
            return
        url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=%s&type=1&offset=0&total=true&limit=%d' % (
            text, 30)
        req = request.Request(url)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
        html = urllib.request.urlopen(req).read()
        text = json.loads(html)
        # print('text', text)
        list_s = text['result']['songs']
        self.listbox_search.delete(0, self.listbox_search.size())
        for i in list_s:
            ids = i['id']
            name = i['name']
            author = i['artists'][0]['name']
            self.listbox_search.insert(END, name + "-" + author)
            self.list_search_id.append(ids)
            self.list_search_name.append(name)
            self.list_search_author.append(author)

    # 下载音乐
    def download(self, url, save_path, name):
        req = request.Request(url)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
        html = urllib.request.urlopen(req).read()
        with open(save_path + '\\' + name, 'wb') as f:
            f.write(html)

    def play_thread(self, id):
        # os.system("ffplay -autoexit -nodisp C:\\Users\\hasee\\Desktop\\music-player\\music-player\\%s" % name)
        # os.system("ffplay -autoexit -nodisp http://music.163.com/song/media/outer/url?id=%d.mp3" % self.list_url[sy])

        os.system("taskkill /F /IM ffplay.exe 2>NUL 1>NUL")
        self.thread = Thread(target=self.paly_http, args=(id,))
        self.thread.setDaemon(True)
        self.thread.start()

    def paly_http(self, id):
        os.system("ffplay -autoexit -nodisp http://music.163.com/song/media/outer/url?id=%d.mp3 2>NUL 1>NUL" % id)

    def paly_myself(self, path, name):
        os.system("ffplay -autoexit -nodisp %s%s" % (path, name))

    def add_play_list(self, event):
        number = self.listbox_search.curselection()[0]
        name = '%s.mp3' % self.list_search_name[number]
        if self.list_search_name[number] in self.list_play_name:
            pass
        else:
            self.list_play_id.append(self.list_search_id[number])
            self.list_play_name.append(self.list_search_name[number])
            self.list_play_author.append(self.list_search_author[number])
            ids = self.list_search_id[number]
            name = self.list_search_name[number]
            author = self.list_search_author[number]
            self.listbox_play.insert(END, name + "-" + author)
            self.write_one_list_txt(name,author,ids)
    def delete_play_list(self,event):
        number = self.listbox_play.curselection()[0]
        print('点击了删除')
        self.list_play_id.pop(number)
        self.list_play_name.pop(number)
        self.list_play_author.pop(number)
        self.listbox_play.delete(number)
        self.delete_one_list_txt(number)

    def click_play_list(self, event):
        number = self.listbox_play.curselection()[0]
        name = '%s.mp3' % self.list_play_name[number]
        self.status = self.start
        self.current_id = number
        os.system("taskkill /F /IM ffplay.exe 2>NUL 1>NUL")
        self.change_id = self.start

    def create_module(self):
        root = Tk()
        root.title("Tkinter Music")
        root.geometry('+300+100')
        self.entry = Entry(root)
        self.entry.grid(row=0, column=0)
        button = Button(root, text='搜索歌曲', command=self.music)
        button.grid(row=1, column=0)

        #搜索列表
        self.listbox_search = Listbox(root, width=50)
        self.listbox_search.bind('<Double-Button-1>', self.add_play_list)
        self.listbox_search.grid(row=2, column=0)

        # 播放列表
        self.listbox_play = Listbox(root, width=50)
        self.listbox_play.bind('<Double-Button-1>', self.click_play_list)
        self.listbox_play.grid(row=3, column=0)

        #播放列表的删除
        self.listbox_play_delete = Listbox(root, width=4)
        self.listbox_play_delete.bind('<Double-Button-1>', self.delete_play_list)
        self.listbox_play_delete.grid(row=3, column=1)


    def main(self):
        mainloop()


if __name__ == '__main__':
    mu = music()
    mu.main()
