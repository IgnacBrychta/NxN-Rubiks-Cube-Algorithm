from tkinter import *
from class_TextScroll import TextScroll
from class_DropDownMenu import DropDownMenu
from tkinter import messagebox
def ScrollWindow_Extract(arg):
	global events
	evens = arg
	print("Restored value:")
	print(events)
def DropDownMenu_extract(arg):
	global session,window
	session = arg
	window.session = arg
class ScrollWindow:
	def __init__(self,dictionary=None,ind=None):
		self.dct = dictionary
		self.session = ind
		self.scrollwindow = Toplevel()
		self.scrollwindow.title("ScrollWindow")
		self.menu = DropDownMenu(self.scrollwindow,items=self.dct,cmd1=self.update_text_box,cmd2=DropDownMenu_extract)
		self.box = TextScroll(self.scrollwindow)
		self.quit_button = Button(self.scrollwindow,text="Quit",command=quit)
		self.quit_button.grid(row=5,column=1,columnspan=2)
		self.add = Button(self.scrollwindow,text="Add",command=lambda: self.entry_cmd(True))
		self.add.grid(row=3,column=1)
		self.remove_button = Button(self.scrollwindow,text="Remove",command=lambda: self.entry_cmd(False))
		self.remove_button.grid(row=3,column=2)
		self.update_text_box()
	def update_text_box(self):
		print("update_text_box")
		print(f"Session: {self.session}")
		self.box.clear()
		for i,x in zip(list(self.dct[self.session]),range(len(list(self.dct[self.session])))):
			self.box.text_box.insert(END,f"{x+1}: {i}")
	def entry_cmd(self,state):
		self.press_arg = state
		self.entry = Entry(self.scrollwindow)
		self.entry.grid(row=4,column=1,columnspan=2)
		if state:
			self.entry.insert(END,"Add an event")
			self.entry.bind("<Key>",self.press)
		else:
			self.entry.insert(END,"Remove an event")
			self.entry.bind("<Key>",self.press)
	def press(self,key):
		global events,session
		print(repr(key.char))
		if key.char == "\r":
			print(self.dct)
			print(self.entry.get())
			if self.dct is not None and self.session is not None:
				if not self.press_arg:
					try:
						if len(list(self.dct.values())) != 1:
							del self.dct[self.entry.get()]
							self.menu.tkinter_drop_down_menu.destroy()
							self.menu = DropDownMenu(self.scrollwindow,items=self.dct,cmd1=self.update_text_box,cmd2=DropDownMenu_extract)
							self.update_text_box()
						else:
							messagebox.showwarning("There Must Be At Least One Event","Action couldn't be completed, since there must be at least one event.")
					except (KeyError,AttributeError):
						try:
							del self.dct[self.session][self.dct[self.session].index(self.entry.get())]
							self.update_text_box()
						except (KeyError,AttributeError,ValueError):
							pass
				else:
					try:
						self.dct[self.session].append(str(float(self.entry.get())))
						self.update_text_box()
					except ValueError:
						print("trying to add something")
						self.dct[self.entry.get()] = []
						self.menu.tkinter_drop_down_menu.destroy()
						self.menu = DropDownMenu(self.scrollwindow,items=self.dct,cmd1=self.update_text_box,cmd2=DropDownMenu_extract)
				ScrollWindow_Extract(self.dct)
	def change(state,info):
		pass
	def quit():
		self.scrollwindow.destroy()