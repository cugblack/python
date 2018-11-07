#!/usr/binn/env python
# -*- coding: utf-8 -*-
import Tkinter

def resize(ev=None):
    hello.config(font="Helvetica -%d bold" % scale.get())

top = Tkinter.Tk()
top.geometry("250 X 150")
#标签
hello = Tkinter.Label(top, text="hello!", font="Helvetica -%d bold")
hello.pack(fill=Y, expand=1)

scale = Tkinter.Scale(top,from_=10, to=40, orient=HORIZONTAL, command=resize)
scale.set(12)
scale.pack(fill=X, expand=1)

#按钮
quit = Tkinter.Button(top, text="quit!", command=top.quit, activeforeground="white", activebackground="red")
quit.pack(fill=Tkinter.X, expand=1)
Tkinter.mainloop()