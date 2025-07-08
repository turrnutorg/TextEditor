VERSION = "1.0"
import sys
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
from tkinter import *

window = Tk()
menubar = Menu(window)
textarea = Text(window)
current_file_path = ""
tit = f"Turrnut text editor v{VERSION}"
ftypes = (
	("All files", "*.*"),	
	("JVM files", "*.java *.kt *.scala"),
	("C/C++ files", "*.h *.hpp *.c *.cpp"),
	("Python files", "*.py"),
	("Static Web files", "*.html *.css"),
	("Rust files", "*.rs"),
	("Ruby files", "*.rb"),
	("Dart files", "*.dart"),
	("Go files", "*.go"),
	("JavaScript/TypeScript files", "*.js  *.ts"),
	("C# Files", "*.cs"),
	("Markdown files", "*.md"),
	("Text files", "*.txt"),
)
cmd = ""

def show():
	global current_file_path
	d = ""
	with open(current_file_path, "r") as fobj:
		d = fobj.readlines()
	textarea.insert("1.0", str(''.join(d)))

def leave(event=None):
	resp = tkinter.messagebox.askquestion("Confirmation", "Do you really want to leave?")
	if resp == "yes":
		sys.exit(0)

def updateName(mod=False):
	global current_file_path
	if current_file_path == "":
		if mod:
			window.title(f"{tit} *")
		else:
			window.title(tit)
		return
	if mod:
		window.title(f"{tit} : \"{current_file_path}\" * ")
	else:
		window.title(f"{tit} : \"{current_file_path}\"")

def helpme(event=None):
	updateName()
	tkinter.messagebox.showinfo(title="Help", message="This is a text editor")
def openF(event=None):
	global current_file_path
	global textarea
	global ftypes
	desired_file = tkinter.filedialog.askopenfile(filetypes=ftypes)
	if desired_file != None:
		textarea.delete("1.0","end")
		current_file_path = os.path.abspath(desired_file.name)
		updateName(mod=False)
		d = desired_file.readlines()
		desired_file.close()
		textarea.insert("1.0", str(''.join(d)))
def save(event=None):
	global textarea
	global current_file_path
	global ftypes
	saved_text = textarea.get("1.0", "end")
	if current_file_path == "":
		file = tkinter.filedialog.asksaveasfilename( defaultextension=ftypes, filetypes=ftypes)
		if file == "":
			return
		with open(file, "w") as fobj:
			current_file_path = os.path.abspath(fobj.name)
			fobj.write(saved_text)
			updateName(mod=False)
	with open(current_file_path, "w") as f:
		f.write(saved_text)
def when_changed(event=None):
	if textarea.edit_modified():
		updateName(mod=True)
	else:
		updateName(mod=False)
def run(event=None):
	global cmd
	global current_file_path
	cmdtemp = tkinter.simpledialog.askstring("Command", "Enter your command, {} will be replaced with the path of file. If you have created commands in this session before you can leave blank.")
	if cmdtemp != None:
		cmd = cmdtemp.replace("{}",f" {current_file_path} ")
	os.system(cmd)

def saveexit(event=None):
	save()
	leave()

textarea.place(x=0,y=0)
window.bind("<<Modified>>", when_changed)
window.bind("<Control-s>", save)
window.bind("<Control-o>", openF)
window.bind("<Control-w>", leave)
window.bind("<Control-r>", run)
window.bind("<Control-e>", saveexit)
window.bind("<Control-h>", helpme)
textarea.configure(font=("Garamond",17),
				   fg="black",
				   bg="white",
				   insertbackground="aqua",
				   wrap="word",
			 relief=SUNKEN,
			 bd=5)
textarea.pack()

fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label="Open(Ctrl+O)", command=openF)

fileMenu.add_command(label="Save(Ctrl+S)", command=save)
fileMenu.add_command(label="Save and Exit(Ctrl+E)", command=saveexit)
fileMenu.add_command(label="Exit(Ctrl+W)", command=leave)
helpMenu = Menu(menubar, tearoff=0)
helpMenu.add_command(label="Help(Ctrl+H)", command=helpme)

runMenu = Menu(menubar, tearoff=0)
runMenu.add_command(label="Run(Ctrl+R)", command=run)

menubar.add_cascade(label="File", menu=fileMenu)
menubar.add_cascade(label="Run", menu=runMenu)
menubar.add_cascade(label="Help", menu=helpMenu)

updateName()
window.geometry("800x600")
window.iconphoto(True, tk.PhotoImage(file="download.png"))
window.resizable(True, True)
#window.overrideredirect(True)
window.protocol("WM_DELETE_WINDOW", leave)
window.configure(bg="#ffffff",menu=menubar)

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		current_file_path = sys.argv[1]
		show()

window.mainloop()
