import cv2
import pyautogui
from win32api import GetSystemMetrics       
import numpy as np

import os
import threading
import time

import tkinter as tk
from tkinter import *
from tkinter import messagebox

from datetime import datetime
#===================SETUP===========================================

def unique_name_file():
   f_name=datetime.now().strftime("%y-%m-%d_%H-%M-%S")
   return f"Record_{f_name}.mp4"

rec_path = r"F:\project\My_screen_recorder"

    #Creates a directory (or folder) — including any intermediate parent folders that don't already exist



#===============================================================

#===========GETTING SYSTEM RESOLUTION==============
widht=GetSystemMetrics(0)
height=GetSystemMetrics(1)
dimension=(widht,height)
#=======================================================


recording=False
output=None
start_time=None

#==============================================================

#======================BUTTON FUNCTION==========================

def s_recording():
    global recording,output,start_time
    recording=True
    os.makedirs(rec_path,exist_ok=True)
    path = os.path.join(rec_path, unique_name_file())
    print(f"[DEBUG] Video will be saved to: {path}")
    
    formate=cv2.VideoWriter_fourcc(*"mp4v")
    output=cv2.VideoWriter(path,formate,30.0,dimension)
    if not output.isOpened():
     print("Failed to open video writer")
     messagebox.showerror("Error", "Unable to create video file!")
     return

    b_start.config(state=tk.DISABLED,bg='gray')
    b_stop.config(state=tk.NORMAL)
    start_time=time.time()
    threading.Thread(target=record_screen,daemon=True).start()
    update_time()
def st_recording():
    global recording
    recording=False
    b_start.config(state=tk.NORMAL)
    b_stop.config(state=tk.DISABLED,bg='gray')
    messagebox.showinfo("Recording","Screen recording saved!")

def record_screen():
    global recording
    print("Recording started")
    while recording:  
     image=pyautogui.screenshot()
     frame_1=np.array(image)
     frame=cv2.cvtColor(frame_1,cv2.COLOR_BGR2RGB)
     output.write(frame)
    output.release()
def update_time():
   if recording:
      elsaped_time=time.time()-start_time
      min=int(elsaped_time//60)
      sec=int(elsaped_time%60)
      timer_label.config(text=f'{min:02}:{sec:02}')
      root.after(1000,update_time)

def close_win():
   root.destroy()
     
#=====================GUI============================
root=tk.Tk()
root.overrideredirect(True)  #to remove title 
root.geometry("600x310")
root.attributes("-alpha", 0.8)
root.config(bg='black')
Label(root,text="Screen Recorder",font=('arial',25),fg='red',bg='black').pack(pady=10)
timer_label=Label(root,text="00:00",font=('arial',25),fg='red',bg='black')
timer_label.pack(pady=10)
b_start=Button(root,text="Start",command=s_recording,fg='red',bg='black')
b_start.pack(pady=10)
b_stop=Button(root,text="Stop",command=st_recording,fg='red',bg='black')
b_stop.pack(pady=5)
c_button=Button(root,text='Close',command=close_win,fg='red',bg='black')
c_button.pack(pady=10)
root.mainloop()
