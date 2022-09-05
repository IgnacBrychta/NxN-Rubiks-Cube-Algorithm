from tkinter import *
"""def DropDownMenu_extract(arg):
	global session
	session = arg
	ScrollWindow.setattr(session = arg)
	print(session)"""
class DropDownMenu:
	def __init__(self,tkinter_root,items={},row=1,column=1,cmd1=None,cmd2=None):
		self.cmd1 = cmd1
		self.cmd2 = cmd2
		self.var = StringVar(tkinter_root)
		self.var.set(list(items.keys())[1])
		self.tkinter_drop_down_menu = OptionMenu(tkinter_root, self.var, *tuple(items.keys()),command=self.change)
		self.tkinter_drop_down_menu.grid(row=row,column=column)
	def change(self,arg):
		self.session = arg
		try: self.cmd2(arg)
		except TypeError: pass
		try: self.cmd1()
		except TypeError: pass
	def __str__(self):
		return "DropDownMenu Class"