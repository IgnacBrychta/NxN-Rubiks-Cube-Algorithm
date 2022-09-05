from tkinter import *
from PIL import ImageTk,Image
import time
def show_image(image):
	global img
	img = ImageTk.PhotoImage(Image.open(image).resize((50,50), Image.ANTIALIAS))
	return img
def QuestionWindowOutput():
	Label(root,text=output).pack()
class QuestionWindow:
	def __init__(self,options,title,info,window_icon=None,box_icon=None):
		self.root = Toplevel()
		self.ind = 1
		self.rw = 1
		self.output = None
		self.root.title(title)
		if window_icon is not None:
			print(window_icon)
			self.root.iconbitmap(window_icon)
		if box_icon is not None:
			self.root_icon = show_image(box_icon)
			print(self.root_icon)
			self.icon_label = Label(self.root,image=self.root_icon)
			#self.icon_label.grid(row=0,column=round(len(options[0])/2))
			self.icon_label.grid(row=1,column=0,rowspan=len(options))
		for ia in range(len(options)):
			for ib in options[ia]:
				self.button = Button(self.root,text=ib,command=lambda var=ib: self.return_(var))
				self.button.grid(row=self.rw,column=self.ind)
				self.ind+=1
				if self.ind == len(options[0])+1:
					self.ind = 1
					self.rw+=1
	def return_(self,button_output):
		global output
		output = button_output
		QuestionWindowOutput()
		self.root.destroy()
				
root = Tk()
root.geometry("200x100")
question = QuestionWindow([["Yellow","Red","Green"],["Orange","Blue","Yellow"]],"Choose a Color","Choose one of the following colors:","settings_icon.ico","YJ.jpg")
root.mainloop()

"""
from tkinter import *
from PIL import ImageTk,Image
import threading
answered = threading.Event()
class QuestionWindow:
	def __init__(self,options,title,info,window_icon=None,box_icon=None):
		self.root = Tk()
		self.ind = 1
		self.rw = 1
		self.output = None
		self.root.title(title)
		if window_icon is not None:
			self.root.iconbitmap(window_icon)
		if box_icon is not None:
			self.root_icon = self.show_image(box_icon)
			self.icon_label = Label(self.root,image=self.root_icon)
			#self.icon_label.grid(row=0,column=round(len(options[0])/2))
			self.icon_label.grid(row=1,column=0,rowspan=len(options))
		for ia in range(len(options)):
			for ib in options[ia]:
				self.button = Button(self.root,text=ib,command=lambda var=ib: self.return_(var))
				self.button.grid(row=self.rw,column=self.ind)
				self.ind+=1
				if self.ind == len(options[0])+1:
					self.ind = 1
					self.rw+=1
		self.root.mainloop()
	def return_(self,button_output):
		global output
		output = button_output
		answered.set()
		self.root.destroy()
	def show_image(self,image):
		global img
		img = ImageTk.PhotoImage(Image.open(image).resize((50,50), Image.ANTIALIAS))
		return img
def main():		
	root = Tk()
	root.geometry("200x100")
	question = threading.Thread(target=lambda: QuestionWindow([["Yellow","Red","Green"],["Orange","Blue","Yellow"]],"Choose a Color","Choose one of the following colors:","settings_icon.ico","YJ.jpg"))
	question.start()
	answered.wait()
	root.mainloop()
if __name__ == '__main__':
	main()
"""