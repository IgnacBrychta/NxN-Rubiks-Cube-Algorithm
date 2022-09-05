from tkinter import *
class TextScroll:
	def __init__(self,root,frame_bd=5,frame_row=2,frame_column=1,frame_columnspan=2,text_box_width=30):
		self.frame = LabelFrame(root,bd=frame_bd)
		self.frame.grid(row=frame_row,column=frame_column,columnspan=frame_columnspan)
		self.scrollbar = Scrollbar(self.frame)
		self.scrollbar.pack(side=RIGHT,fill=Y)
		self.text_box = Listbox(self.frame,yscrollcommand=self.scrollbar.set,width=text_box_width)
		self.text_box.pack(side=LEFT,fill=BOTH)
		self.scrollbar.config(command=self.text_box.yview)
	def clear(self):
		self.text_box.delete(0,END)
	def __str__(self):
		return "TextScroll Class"