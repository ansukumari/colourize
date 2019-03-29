from tkinter import ttk
import tkinter as tk, os
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox as mb

def openPic(pic_path):
    pic = Image.open(pic_path)
    h, w = 600, 500
    if pic.size[1] > h: pic = pic.resize((int(h*pic.size[0]/pic.size[1]), h), Image.ANTIALIAS)
    if pic.size[0] > w: pic = pic.resize((w, int(w*pic.size[1]/pic.size[0])), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(pic)

    picpop = tk.Toplevel()
    picpop.geometry('500x600')
    picpop.title('Image Preview')
    tk.Label(picpop, image=photo, bg='white').pack()
    picpop.mainloop()

def browse(wid):
    filename = filedialog.askdirectory()
    if filename: wid.configure(text=filename)

def execute(file): 
    inp = Image.open(file).convert('LA')
    return inp

'''Top Level/Root'''
root = tk.Tk()
root.title("Colourize")
root.geometry('900x550')

'''LG Logo Banner'''
photo = ImageTk.PhotoImage(Image.open('img/banner.png'))
tk.Label(root, image=photo, bg='white').place(relx=0, rely=0, relwidth=1, relheight=0.15)

''' Tab Styling (Padding) '''
btn_width = 15
col1, col2, col3, col4 = 0.1, 0.25, 0.5, 0.7
row1, row2, row3, row4 = 0.1, 0.25, 0.4, 0.8
mygreen = "#d2ffd2"
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
    "TNotebook": {"configure": {"background": 'lightgrey'} },
    "TNotebook.Tab": {
        "configure": {"padding": [20, 10], "background": 'lightgrey' },
        "map":       {"background": [("selected", root.cget('bg'))], }
    },
})
style.theme_use("MyStyle")

''' Notebook Creation '''
nb = ttk.Notebook(root)
nb.place(rely=0.15, relwidth=1, relheight=0.85)

''' Notebook Pages '''
p1 = ttk.Frame(nb)
p2 = ttk.Frame(nb)

nb.add(p1, text='Select File')
nb.add(p2, text='Select Folder')


''' Page# 1 | Select File'''

tk.Label(p1, text='Input File').place(relx=col1, rely=row1)
path_file = tk.Label(p1, text=os.getcwd() + '/img/default.png')
def browseFile():
    filename = filedialog.askopenfilename(filetypes=(('', '*.jpg'), ('', '*.jpeg'), ('', '*.png')))
    if filename: path_file.configure(text=filename)
    refresh_file()
tk.Button(p1, text='Browse', width=btn_width, command=browseFile).place(relx=col4, rely=row1)
path_file.place(relx=col2, rely=row1)

fr_inp = tk.Frame(p1)
fr_inp.place(relx=col1, rely=row2, relheight=0.47, relwidth=0.36)
tk.Label(fr_inp, text='Input Image').pack(side='top')
de_img = Image.open(os.getcwd() + '/img/default.png')
de_img = de_img.resize((320, 190), Image.ANTIALIAS)
default_img = ImageTk.PhotoImage(de_img)
in_img = tk.Label(fr_inp, image=default_img)
in_img.pack()


fr_op = tk.Frame(p1)
fr_op.place(relx=col3, rely=row2, relheight=0.47, relwidth=0.36)
tk.Label(fr_op, text='Output Image').pack(side='top')
op_img = tk.Label(fr_op, image=default_img)
op_img.pack()

def refresh_file():
    c_img = Image.open(path_file.cget('text'))
    w, h = 320, 180
    if c_img.size[1] < h: c_img = c_img.resize((int(h*c_img.size[0]/c_img.size[1]), h), Image.ANTIALIAS)
    if c_img.size[0] < w: c_img = c_img.resize((w, int(w*c_img.size[1]/c_img.size[0])), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(c_img)
    in_img.configure(image=img)
    in_img.image = img

def process_file():
    file = execute(path_file.cget('text'))
    name = path_file.cget('text').rpartition('.')[0]
    file.save(name+'_greyscale.png')
    w, h = 320, 180
    if file.size[1] < h: file = file.resize((int(h*file.size[0]/file.size[1]), h), Image.ANTIALIAS)
    if file.size[0] < w: file = file.resize((w, int(w*file.size[1]/file.size[0])), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(file)
    op_img.configure(image=img)
    op_img.image = img

tk.Label(p1, text='*output location is same as input location').place(relx=col1, rely=row4)
tk.Button(p1, text='Process', width=btn_width, command=process_file).place(relx=col4, rely=row4)

''' Page# 2 | Select Folder '''

tk.Label(p2, text='Input Folder').place(relx=col1, rely=row1)
path_inp = tk.Label(p2, text=os.getcwd() + '/unprocessed')
def browseInp():
    browse(path_inp)
    refersh_inp()
tk.Button(p2, text='Browse', width=btn_width, command=browseInp).place(relx=col4, rely=row1)
path_inp.place(relx=col2, rely=row1)

tk.Label(p2, text='Output Folder').place(relx=col1, rely=row2)
path_op = tk.Label(p2, text=os.getcwd() + '/processed')
def browseOp():
    browse(path_op)
    refersh_op()
tk.Button(p2, text='Browse', width=btn_width, command=browseOp).place(relx=col4, rely=row2)
path_op.place(relx=col2, rely=row2)

fr_inp = tk.Frame(p2)
fr_inp.place(relx=col1, rely=row3, relheight=0.3, relwidth=0.36)
yscroll = tk.Scrollbar(fr_inp, orient=tk.VERTICAL)
lst_inp = tk.Listbox(fr_inp, yscrollcommand=yscroll.set)
yscroll.config(command=lst_inp.yview)
yscroll.pack(side='right', fill='y')
tk.Label(fr_inp, text='Unprocessed Files').pack(side='top')
lst_inp.pack(side='left', fill='both', expand=1)
def showPic(event): openPic(path_inp.cget('text')+'/'+event.widget.get(event.widget.curselection()))
lst_inp.bind('<Double-Button>', showPic)

def refersh_inp():
    lst_inp.delete(0, 'end')
    for f in os.listdir(path_inp.cget('text')): lst_inp.insert('end', f)
refersh_inp()

fr_op = tk.Frame(p2)
fr_op.place(relx=col3, rely=row3, relheight=0.3, relwidth=0.36)
yscroll = tk.Scrollbar(fr_op, orient=tk.VERTICAL)
lst_op = tk.Listbox(fr_op, yscrollcommand=yscroll.set)
yscroll.config(command=lst_op.yview)
yscroll.pack(side='right', fill='y')
tk.Label(fr_op, text='Processed Files').pack(side='top')
lst_op.pack(side='left', fill='both', expand=1)
def showPic(event): openPic(path_op.cget('text')+'/'+event.widget.get(event.widget.curselection()))
lst_op.bind('<Double-Button>', showPic)

def refersh_op():
    lst_op.delete(0, 'end')
    for f in os.listdir(path_op.cget('text')): 
        if not f[0] == '.': lst_op.insert('end', f)
refersh_op()

def process(): 
    for f in os.listdir(path_inp.cget('text')):
        op = execute(path_inp.cget('text')+'/'+f)
        op.save(path_op.cget('text')+'/'+f.rpartition('.')[0]+'_greyscale.png')
        refersh_op()

tk.Button(p2, text='Process', width=btn_width, command=process).place(relx=col4, rely=row4)

root.resizable(0,0)
root.mainloop()
