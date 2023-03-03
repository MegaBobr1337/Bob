from tkinter import *

root = Tk()

root.title('helper')
root.geometry('400x600')
root.resizable(width=False, height=False)
root.iconbitmap("icon\icon.ico")

canvas = Canvas(root, height=300,width=250)
canvas.pack()

frame = Frame(root)
frame.place(relx=0,rely=0.3,relheight=0.7, relwidth=1)
title = Label(frame, text="Нажмите на кнопку и говорите", font=("Arial",20))
title.pack()
btn = Button(frame, text='Кнопка',bg='gray',width=15, height=3,font=("Arial",20))
btn.pack(pady=50)

root.mainloop()