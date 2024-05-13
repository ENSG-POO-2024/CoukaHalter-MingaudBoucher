# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:57:42 2024

@author: Formation
"""

import tkinter
from tkinter import messagebox, Button
from tkinter import *

gui = Tk()
gui.geometry("200x150")

def msgCallBack_An():
    messagebox.showinfo("App", "Attaque neutre")
    return(True)

def msgCallBack_At():
    messagebox.showinfo("App", "Attaque type")
    return(True)
    
def msgCallBack_changes():
    messagebox.showinfo("App", "Changement de pokemon")
    return(True)

def msgCallBack_fuite():
    messagebox.showinfo("App", "Fuite du joueur")
    return(True)
    
btn1 = Button(
  gui,
  text = 'attaque neutre',
  command = msgCallBack_An, 
  activeforeground = "green",
  activebackground = "yellow",
  padx = 8,
  pady = 5
)
btn2 = Button(
  gui, 
  text = 'attaque type',
  command = msgCallBack_At,
  activeforeground = "blue",
  activebackground = "yellow",
  padx = 8,
  pady = 5
)
btn3 = Button(
  gui, 
  text = 'changer de pokemon',
  command = msgCallBack_changes,
  activeforeground = "red",
  activebackground = "yellow",
  padx = 8,
  pady = 5
)
btn4 = Button(
  gui, 
  text = 'fuite',
  command = msgCallBack_fuite,
  activeforeground = "black",
  activebackground = "yellow",
  padx = 8,
  pady = 5
)

btn1.pack(side = LEFT)
btn2.pack(side = RIGHT)
btn3.pack(side = TOP)
btn4.pack(side = BOTTOM)
gui.mainloop()