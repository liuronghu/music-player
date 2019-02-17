# _*_ coding:utf-8 _*_
import os
from tkinter import *
from tkinter import messagebox
import urllib
import json
import mp3play
from urllib import request
import urllib

class music(object):
    def __init__(self):
        self.list_url = []
        self.list_name = []

    def music(self):
        self.list_url = []
        self.list_name = []
        text = self.entry.get()
        text = text.encode('utf-8')
        text = request.quote(text)
        if not text:
            messagebox.showinfo('温馨提示', '您可以输入以下内容进行搜索\n1.歌曲名\n2.歌手名\n3.部分歌词')
            return
        data = request.quote('胡歌')
        url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=%s&type=1&offset=0&total=true&limit=10' % data
        req = request.Request(url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
        html = urllib.request.urlopen(req).read()
        text = json.loads(html)
        print('text', text)
        list_s = text['result']['songs']
        self.listbox.delete(0, self.listbox.size())
        for i in list_s:
            self.listbox.insert(END, i['name'] + "(" + i['artists'][0]['name'] + ")")
            self.list_url.append(i['id'])
            self.list_name.append(i['name'])

    def play(self, event):
        sy = self.listbox.curselection()[0]
        name = '%s.mp3' % self.list_name[sy]
        if os.path.isfile(name):
            #os.system(name)
            os.system("ffplay -autoexit -nodisp C:\\Users\\hasee\\Desktop\\music-player\\music-player\\%s" % name)
            #mp3 = mp3play.load(name)
            # mp3 = mp3play.load('http://music.163.com/song/media/outer/url?id=%d.mp3' % self.list_url[sy])
            #mp3.play()
        else:
            url = r'http://music.163.com/song/media/outer/url?id=%d.mp3' % self.list_url[sy]
            req = request.Request(url)
            req.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36")
            html = urllib.request.urlopen(req).read()
            with open(name, 'wb') as f:
                f.write(html)
            #os.system(name)
            os.system("ffplay -autoexit -nodisp C:\\Users\\hasee\\Desktop\\music-player\\music-player\\指纹.mp3")
            #mp3 = mp3play.load(name)
            #mp3.play()


    def main(self):
        root = Tk()
        root.title("Tkinter Music")
        root.geometry('+300+100')
        self.entry = Entry(root)
        self.entry.pack()
        button = Button(root, text='搜索歌曲', command=self.music)
        button.pack()
        self.listbox = Listbox(root, width=50)
        self.listbox.bind('<Double-Button-1>', self.play)
        self.listbox.pack()
        mainloop()


mu = music()
mu.main()
