from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import subprocess
import random as r
from threading import Thread
import os
import time


TitleEmojis = ["ヾ(≧▽≦*)o","o(*//▽//*)q","ヾ(•ω•`)o","(っ °Д °;)っ","o((>ω< ))o","(。>︿<)_θ","w(ﾟДﾟ)w"]
LastText = 3.3
History = []
LastOutput = 0
output = ""
error = ""
CommandComplete = True
AnimationFinish =  False
Debug = False
CantRun = ["cmd","python"]
DisableCommand = ["dir","start","shutdown",""," ","pip"]
try:
    with open("data/config.txt","r",encoding="utf-8") as file:
        TranslateText = eval(file.read())
        if type(TranslateText) != dict:
            raise TypeError
except Exception as e:
    messagebox.showerror("KawaiCmd",f"配置文件缺失/格式错误!(./data/config.txt)\n{e}")
    quit()


def StartAnimation():
    global AnimationFinish

    time.sleep(3)
    AnimationFinish = True

def ChangeDebug():
    global Debug

    Debug = not Debug
    messagebox.showinfo("Debug",f"Debug={Debug}")

root = Tk()
root.title("KawaiCmd")
root.geometry("800x400")
root.attributes("-alpha", 0.9)
root.resizable(False, False)

c = Canvas(root, bg="black", height=400, width=800, highlightthickness=0)
c.pack()
text = Label(root, text="KawaiCmd", font=("Consolas", 50), bg="black", fg="white")
c_text = c.create_window(400,170,window=text)
Thread(target=StartAnimation,daemon=True).start()
while not AnimationFinish:
    root.update()
c.destroy()

text = Text(root, wrap=WORD, width=130, height=31, font=("Consolas", 14), bg="#FFC0CB", fg="black", relief="flat")
text.insert(INSERT, "~{}~ Kawai_Cmd v1.0 By QingLanStudio\n{}\n>>>".format(r.choice(TitleEmojis),"-"*45))
text.config(state=DISABLED)
text.pack()

menu = Menu(root,tearoff=0)
root.config(menu=menu)
menu.add_command(label="关于~",command=lambda: messagebox.showinfo("关于KawaiCmd","KawaiCmd v1.0是由青岚工作室制作的CMD魔改版\n这个版本让CMD的提示变得更可愛い,同时加入了自定义配置文件\n让用户自己修改提示风格\n目前已知问题:部分命令无法使用(例如color,cmd等),输入太快会导致删除无法使用(cls一下即可)\n输入部分错误命令会一直报'&&'错误(cls一下即可)"))
menu.add_command(label="窗口透明度设定~",command=lambda: root.attributes("-alpha",simpledialog.askfloat("KawaiCmd","请输入透明度(0.1-1):",initialvalue=0.9,minvalue=0.1,maxvalue=1)))
menu.add_command(label="自定义配置文件~",command=lambda: (os.system(f"start {os.curdir}/data/config.txt"),messagebox.showinfo("自定义配置文件","配置文件路径:./data/config.txt\n配置文件格式:字典\n原文本:替换文本\n例如:\n{'原文本':'替换文本'}\n注意:原文本和替换文本都需要用引号括起来\n配置文件错误会导致程序无法运行!")))
menu.add_command(label="Debug Change!",command=ChangeDebug)


def InputText(event):
    global LastText
    global Debug

    text.config(state=NORMAL)
    cursorpos = text.index(INSERT)
    print("[IN]Cursor at",cursorpos) if Debug else None
    if float(str(cursorpos).split(".")[1]) >= float(str(LastText).split(".")[1]) and str(cursorpos).split(".")[0] == str(LastText).split(".")[0]:
        text.insert(INSERT,event.char)
    else:
        print("[IN]Cursor out of writeable area") if Debug else None
        text.mark_set(INSERT,END)
    text.config(state=DISABLED)

def DeleteText(event):
    global LastText
    global Debug

    text.config(state=NORMAL)
    cursorpos = text.index(INSERT)
    cursorcol = float(str(cursorpos).split(".")[1])
    delcol = float(str(LastText).split(".")[1]) + 1

    print(f"[DEL]Trying to delete {cursorpos},LastText=",LastText) if Debug else None
    print("[DEL]Now Col/Del Col:",cursorcol,delcol) if Debug else None
    if cursorcol >= delcol and str(cursorpos).split(".")[0] == str(LastText).split(".")[0]:
        text.delete(f"{cursorpos}-1c")
        print("[DEL]Deleted "+cursorpos) if Debug else None
    else:
        text.mark_set(INSERT,END)
        print("[DEL]Out of DelArea") if Debug else None

    text.config(state=DISABLED)

def RunCommand(History,runtext):
    global output,error
    global CommandComplete
    global DisableCommand
    global CantRun
    global Debug

    if CommandComplete == True:
        print(f"[CMD]Running {runtext}") if Debug else None
        CommandComplete = False
        if (any(runtext.startswith(i) for i in DisableCommand) or any(runtext.startswith(j) for j in CantRun)) and len(History) > 1:
            History.pop(-1)
        command = subprocess.run("&&".join(History) if len(History) > 1 else runtext,text=True,capture_output=True,shell=True)
        print(f"[CMD]All Output:{command.stdout.strip()}\nLast ComPos={LastOutput}") if Debug else None
        output,error = command.stdout[LastOutput:].strip(),command.stderr.strip()
        CommandComplete = True
        print(f"[CMD]History:{History}") if Debug else None
    else:
        messagebox.showerror("KawaiCmd","上一个命令还未执行完毕!")

def NextText(event):
    global LastText
    global TranslateText
    global CantRun
    global History
    global LastOutput
    global output,error
    global CommandComplete
    global Debug

    text.config(state=NORMAL)
    runtext = text.get(LastText,INSERT)
    print("[COM]Pressed Enter") if Debug else None
    if runtext == "exit":
        print("[COM]Quited") if Debug else None
        quit()
    elif runtext == "cls":
        print("[COM]Cleared") if Debug else None
        History = []
        LastText = 3.3
        LastOutput = 0
        output = ""
        error = ""
        text.config(state=NORMAL)
        text.delete("1.0",END)
        text.insert(INSERT, "~{}~ Kawai_Cmd v1.0 By QingLanStudio\n{}\n>>>".format(r.choice(TitleEmojis),"-"*45))
        text.mark_set(INSERT,END)
        text.config(state=DISABLED)
    elif runtext in CantRun:
        print("[COM]Cant run") if Debug else None
        messagebox.showwarning("KawaiCmd","该命令不受支持,请在原版Cmd中运行!")
        text.insert(INSERT,"\n\n>>>")
        LastText += 2
    else:
        History.append(runtext)
        text.config(state=DISABLED)
        Thread(target=RunCommand,args=(History,runtext),daemon=True).start()
        while not CommandComplete:
            root.update()
        text.config(state=NORMAL)

        if error == "":
            for origintext,translatetext in TranslateText.items():
                output = output.replace(origintext,translatetext)
            text.insert(INSERT,f"\n{output}\n>>>")
            LastText += 2 + output.count("\n")
            LastOutput += len(output)
        else:
            History.pop(-1)
            for origintext,translatetext in TranslateText.items():
                error = error.replace(origintext,translatetext)
            text.insert(INSERT,f"\n{error}\n>>>")
            LastText += 2 + error.count("\n")

    text.mark_set(INSERT,str(LastText+0.1))
    text.see(INSERT)
    text.config(state=DISABLED)

root.bind("<Key>", InputText)
root.bind("<BackSpace>", DeleteText)
root.bind("<Return>",NextText)
root.mainloop()